import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';

export class VpcStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    const vpc = new ec2.Vpc(this, 'VPC');

    new cdk.CfnOutput(this, 'VpcId', {
      value: vpc.vpcId,
      description: 'VPC ID', // Optional
    });

    new cdk.CfnOutput(this, 'Public Subnets', {
      value: vpc.publicSubnets.toString(),
      description: 'Public Subnets', // Optional
    });

    new cdk.CfnOutput(this, 'Private Subnets', {
      value: vpc.privateSubnets.toString(),
      description: 'Private Subnets', // Optional
    });
  }
}
