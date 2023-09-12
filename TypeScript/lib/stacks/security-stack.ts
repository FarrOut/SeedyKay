import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { IamNestedStack } from '../components/security/iam-nestedstack';



export class SecurityStack extends cdk.Stack {

    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        let IamStack = new IamNestedStack(this, 'IamNestedStack', {
            RemovalPolicy: cdk.RemovalPolicy.DESTROY,
        })
    }
}
