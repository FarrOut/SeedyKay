import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import { Port, SecurityGroup } from '@aws-cdk/aws-ec2';

export class TestStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'VPC');

    //  Security group
    const redisSecurityGroup = new SecurityGroup(this, 'edpuzzleRedisSecurityGroup', {
      vpc, // VPC from the baseStack
      allowAllOutbound: true,
      description: 'Security Group for Redis Dev',
      securityGroupName: 'redis-security-group-development'
    })

    const defaultSecurityGroupFromVpc = SecurityGroup.fromSecurityGroupId(this, 'defaultSG',
      vpc.vpcDefaultSecurityGroup
   )

    redisSecurityGroup.addIngressRule(defaultSecurityGroupFromVpc, Port.tcp(6379))
  }
}
