import {CfnResource, RemovalPolicy, Stack, StackProps} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as opensearch from 'aws-cdk-lib/aws-opensearchservice';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import {Domain, ElasticsearchVersion} from "aws-cdk-lib/aws-elasticsearch";

export class ElasticsearchStack extends Stack {
    constructor(scope: Construct, id: string, ElasticsearchVersion: ElasticsearchVersion, props?: StackProps) {
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

        const domain = new Domain(this, 'Domain', {
            version: ElasticsearchVersion,
            enableVersionUpgrade: true, // defaults to false
        });

        domain.node.addDependency(serviceLinkedRole);
    }
}
