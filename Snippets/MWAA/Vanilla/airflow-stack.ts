import * as cdk from 'aws-cdk-lib';
import {aws_ec2 as ec2, aws_iam as iam, aws_mwaa as mwaa, aws_s3 as s3, CfnOutput, RemovalPolicy} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {CompositePrincipal, Effect} from "aws-cdk-lib/aws-iam";

export class AirflowStack extends cdk.Stack {
    constructor(scope: Construct, id: string, Vpc: ec2.Vpc, props?: cdk.StackProps) {
        super(scope, id, props);

        const securityGroup = new ec2.SecurityGroup(this, 'SG', {
            vpc: Vpc,
            allowAllOutbound: false,
        });

        const SourceBucket = new s3.Bucket(this, 'SourceBucket',
            {
                autoDeleteObjects: true,
                removalPolicy: RemovalPolicy.DESTROY,
            }
        );

        const ExecutionRole = new iam.Role(this, 'ExecutionRole', {
            assumedBy: new CompositePrincipal(new iam.ServicePrincipal("airflow.amazonaws.com"),
                new iam.ServicePrincipal("airflow-env.amazonaws.com")),
            description: 'ExecutionRole for MWAA',
        });
        ExecutionRole.applyRemovalPolicy(RemovalPolicy.DESTROY)

        //Grant access to Amazon S3 bucket with account-level public access block
        //https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-create-role.html#mwaa-create-role-s3-publicaccessblock
        ExecutionRole.addToPolicy(new iam.PolicyStatement({
            effect: Effect.ALLOW,
            actions: ["s3:GetAccountPublicAccessBlock"],
            resources: ['*'],
        }))

        // ExecutionRole.addManagedPolicy(
        //     ManagedPolicy.fromManagedPolicyArn(this, 'AmazonMWAAServiceRolePolicy',
        //         'arn:aws:iam::aws:policy/aws-service-role/AmazonMWAAServiceRolePolicy'))
        SourceBucket.grantReadWrite(ExecutionRole);

        const Airflow = new mwaa.CfnEnvironment(this, 'MyAirflowEnvironment', {
            name: 'AirFlow',
            networkConfiguration: {
                securityGroupIds: [securityGroup.securityGroupId],
                subnetIds: ['subnet-xxxxxxxxxx', 'subnet-xxxxxxxxx'],
            },
            sourceBucketArn: SourceBucket.bucketArn,
            dagS3Path: 'airflow/dags/',
            executionRoleArn: ExecutionRole.roleArn,
        });

        new CfnOutput(this, 'AirflowWebserverUrl',
            {
                value: Airflow.attrWebserverUrl,
                description: '',
            }
        )
    }
}
