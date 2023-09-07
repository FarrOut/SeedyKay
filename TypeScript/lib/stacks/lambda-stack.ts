import { VpcNestedStack } from '../components/networking/vpc-nestedstack';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { AlwaysUpdatingLambdaFunctionStack } from '../components/compute/lambda/always-updating-lambda-function-stack';

/* ===============================================================================
// === References ===
// [1] - SubnetFilter.byIds
// https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.SubnetFilter.html#static-bywbridssubnetids


===============================================================================*/

export class LambdaStack extends cdk.Stack {

    public readonly functionArn: string;

    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        let LambdaStack = new AlwaysUpdatingLambdaFunctionStack(this, 'AlwaysUpdatingLambdaFunctionStack')
        this.functionArn = LambdaStack.function.functionArn;
        new cdk.CfnOutput(this, 'LambdaFunctionArn', {
            value: this.functionArn,
            description: 'Lambda function ARN',
        })
    }
}
