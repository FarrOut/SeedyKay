import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import { VpcNestedStack } from '../components/networking/vpc-nestedstack';

/* ===============================================================================
// === References ===
// [1] - SubnetFilter.byIds
// https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.SubnetFilter.html#static-bywbridssubnetids


===============================================================================*/

export class NetworkStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    let Vpc = new VpcNestedStack(this, 'VpcNestedStack',)

    


  }
}
