import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';

/* ===============================================================================
// === References ===
// [1] - SubnetFilter.byIds
// https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.SubnetFilter.html#static-bywbridssubnetids


===============================================================================*/

export class DemoStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpcId = 'vpc-xxxxxxxxxxxxxxxxx'
    const pub_subnet_a = 'subnet-xxxxxxxxxxxxxxxxx'
    const pub_subnet_b = 'subnet-xxxxxxxxxxxxxxxxx'

    const priv_subnet_a = 'subnet-xxxxxxxxxxxxxxxxx'
    const priv_subnet_b = 'subnet-xxxxxxxxxxxxxxxxx'

    // ===========
    // CONTROL
    // ===========
    // https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.Subnet.html#static-fromwbrsubnetwbridscope-id-subnetid
    const pub_control_subnet_a = ec2.Subnet.fromSubnetId(this, 'PublicSubnetFromId', pub_subnet_a);
    new cdk.CfnOutput(this, 'PublicControlSubnet', {
      value: pub_control_subnet_a.subnetId,
      description: 'Public Control Subnet', // Optional
    });

    const priv_control_subnet_a = ec2.Subnet.fromSubnetId(this, 'PrivateSubnetFromId', priv_subnet_a);
    new cdk.CfnOutput(this, 'PrivateControlSubnet', {
      value: priv_control_subnet_a.subnetId,
      description: 'Private Control Subnet', // Optional
    });

    // ===========
    // EXPERIMENT
    // ===========

    const vpc = ec2.Vpc.fromLookup(this, 'VPC', {
      // This imports the default VPC but you can also
      // specify a 'vpcName' or 'tags'.
      vpcId: vpcId,
    });

    const publicSubnets = vpc.selectSubnets(
      { subnetFilters: [ec2.SubnetFilter.byIds([pub_subnet_a, pub_subnet_b])] }
    )

    new cdk.CfnOutput(this, 'PublicSubnetsExperiment', {
      value: publicSubnets.subnetIds.toString(),
      description: 'Public Subnets', // Optional
    });

    const privateSubnets = vpc.selectSubnets(
      { subnetFilters: [ec2.SubnetFilter.byIds([priv_subnet_a, priv_subnet_b])] }
    )

    new cdk.CfnOutput(this, 'PrivateSubnetsExperiment', {
      value: privateSubnets.subnetIds.toString(),
      description: 'Private Subnets', // Optional
    });

    const mixedSubnets = vpc.selectSubnets(
      { subnetFilters: [ec2.SubnetFilter.byIds([priv_subnet_a, pub_subnet_a])] }
    )

    new cdk.CfnOutput(this, 'MixedSubnetsExperiment', {
      value: mixedSubnets.subnetIds.toString(),
      description: 'Mixed Public and Private Subnets', // Optional
    });


  }
}
