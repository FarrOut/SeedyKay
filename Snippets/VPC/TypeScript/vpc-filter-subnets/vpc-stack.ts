import * as ec2 from '@aws-cdk/aws-ec2';

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

export class VpcStack extends cdk.NestedStack {

  public readonly vpc: ec2.IVpc;

  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    this.vpc = new ec2.Vpc(this, 'VPC');

    new cdk.CfnOutput(this, 'VpcId', {
      value: this.vpc.vpcId,
      description: 'VPC ID', // Optional
    });

    new cdk.CfnOutput(this, 'Public Subnets', {
      value: this.vpc.publicSubnets.toString(),
      description: 'Public Subnets', // Optional
    });

    new cdk.CfnOutput(this, 'Private Subnets', {
      value: this.vpc.privateSubnets.toString(),
      description: 'Private Subnets', // Optional
    });
  }
}
