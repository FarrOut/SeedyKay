import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as logs from 'aws-cdk-lib/aws-logs';
import {AlwaysUpdatingLambdaFunctionStack} from "../../compute/lambda/always-updating-lambda-function-stack";

interface MyProps {
    LogGroup?: logs.ILogGroup,
    removalPolicy?: cdk.RemovalPolicy,
    testType: TestType,
}

enum TestType {
    INTEGRATION,
    REGRESSION,
    UNIT,
    SMOKE
}

export class TestingStage extends cdk.Stage {


    constructor(scope: Construct, id: string, props: MyProps) {
        super(scope, id, props);

        new AlwaysUpdatingLambdaFunctionStack(this, 'TestingFunction',
            {
                removalPolicy: props.removalPolicy,
            })

        // CfnOutput(this, 'TestType', value:props.testType. )
    }
}