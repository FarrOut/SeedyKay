import {VpcNestedStack} from '../components/networking/vpc-nestedstack';
import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';

/* ===============================================================================
// === References ===
// [1] - SubnetFilter.byIds
// https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.SubnetFilter.html#static-bywbridssubnetids


===============================================================================*/

export class NetworkStack extends cdk.Stack {

    public readonly VpcId: string;

    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        let Vpc = new VpcNestedStack(this, 'VpcNestedStack',)

        this.VpcId = Vpc.vpc.vpcId


    }
}
