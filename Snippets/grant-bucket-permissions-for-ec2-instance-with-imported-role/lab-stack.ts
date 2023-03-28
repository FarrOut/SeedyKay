import {CfnOutput, RemovalPolicy, Stack, StackProps} from 'aws-cdk-lib';
import {Construct} from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class LabStack extends Stack {
    constructor(scope: Construct, id: string, key_name: string, roleArn: string, props?: StackProps) {
        super(scope, id, props);


        const vpc = new ec2.Vpc(this, 'VPC');

        const role = iam.Role.fromRoleArn(this, 'Role', roleArn, {
            // Set 'mutable' to 'false' to use the role as-is and prevent adding new
            // policies to it. The default is 'true', which means the role may be
            // modified as part of the deployment.
            mutable: true,
        });

        const mySecurityGroup = new ec2.SecurityGroup(this, 'SecurityGroup', {
            vpc,
            description: 'Allow ssh access to ec2 instances',
            allowAllOutbound: true   // Can be set to false
        });
        mySecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22), 'allow ssh access from the world');

        // AWS Linux
        const instance = new ec2.Instance(this, 'Instance1', {
            vpc,
            instanceType: ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.LARGE,
            ),
            machineImage: new ec2.AmazonLinuxImage(),
            role: role,
            keyName: key_name,
            securityGroup: mySecurityGroup,
            vpcSubnets: {
                subnetType: ec2.SubnetType.PUBLIC,
            },
        });

        let user = 'ec2-user'
        let ssh_command = 'ssh' + ' -i \"' + key_name + '.pem\" ' + user + '@' + instance.instancePublicDnsName

        new CfnOutput(this, 'InstanceSSHcommand', {
            value: ssh_command,
            description: 'Command to SSH into instance.'
        });

        const bucket = new s3.Bucket(this, 'MyFirstBucket',
            {autoDeleteObjects: true,}
        );

        bucket.grantReadWrite(role)
        bucket.applyRemovalPolicy(RemovalPolicy.DESTROY)

        new CfnOutput(this, 'BucketName', {
            value: bucket.bucketName,
            description: 'Bucket Name'
        });
    }
}
