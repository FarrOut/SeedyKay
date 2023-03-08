import {CfnResource, RemovalPolicy, Stack, StackProps} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as opensearch from 'aws-cdk-lib/aws-opensearchservice';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class OpenSearchStack extends Stack {
    constructor(scope: Construct, id: string, OpenSearchVersion: opensearch.EngineVersion, props?: StackProps) {
        super(scope, id, props);

        const vpc = new ec2.Vpc(this, 'VPC', {
            maxAzs: 2,
        });

        const serviceLinkedRole = new CfnResource(this, "es-service-linked-role", {
            type: "AWS::IAM::ServiceLinkedRole",
            properties: {
                AWSServiceName: "es.amazonaws.com",
                Description: "Role for ES to access resources in my VPC"
            }
        });

        const domain = new opensearch.Domain(this, 'Domain', {
            version: OpenSearchVersion,
            enableVersionUpgrade: true, // defaults to false
            removalPolicy: RemovalPolicy.DESTROY,
            vpc,
            // must be enabled since our VPC contains multiple private subnets.
            zoneAwareness: {
                enabled: true,
            },
            capacity: {
                // must be an even number since the default az count is 2.
                dataNodes: 2,
            },
        });

        domain.node.addDependency(serviceLinkedRole);
    }
}
