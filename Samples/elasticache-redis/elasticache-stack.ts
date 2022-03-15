import {CfnResource, RemovalPolicy, Stack, StackProps} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as elasticache from 'aws-cdk-lib/aws-elasticache';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class ElastiCacheStack extends Stack {
    constructor(scope: Construct, id: string, RedisEngineVersion: string, props?: StackProps) {
        super(scope, id, props);

        const vpc = ec2.Vpc.fromLookup(this, 'VPC', {
            // This imports the default VPC but you can also
            // specify a 'vpcName' or 'tags'.
            isDefault: true,
        });

        const securityGroup = new ec2.SecurityGroup(this, 'ElastiCacheSG', {
            allowAllOutbound: false,
            description: "ElastiCacheSG",
            disableInlineRules: false,
            securityGroupName: "ElastiCacheSG",
            vpc: vpc,

        });

        const cluster = new elasticache.CfnCacheCluster(this, 'MyCfnCacheCluster', {
            engine: 'redis',
            cacheNodeType: "cache.t2.micro",
            numCacheNodes: 1,
            vpcSecurityGroupIds: [securityGroup.securityGroupId],
            autoMinorVersionUpgrade: true,
            engineVersion: RedisEngineVersion,
        })

    }
}
