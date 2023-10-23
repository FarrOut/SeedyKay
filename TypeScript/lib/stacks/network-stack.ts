import {VpcNestedStack} from '../components/networking/vpc-nestedstack';
import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
/* ===============================================================================
// === References ===
// [1] - SubnetFilter.byIds
// https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.SubnetFilter.html#static-bywbridssubnetids


===============================================================================*/

export class NetworkingStack extends cdk.Stack {

    public readonly Vpc: ec2.IVpc;

    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        this.Vpc = new VpcNestedStack(this, 'VpcNestedStack',).vpc



    }
}
