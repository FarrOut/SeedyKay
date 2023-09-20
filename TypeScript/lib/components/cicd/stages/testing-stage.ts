import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as logs from 'aws-cdk-lib/aws-logs';
import {LambdaStack} from "../../../stacks/lambda-stack";

interface MyProps extends cdk.StageProps {
    LogGroup?: logs.ILogGroup,
    removalPolicy: cdk.RemovalPolicy,
    testType: TestType,
}

export enum TestType {
    INTEGRATION = 'Integration',
    REGRESSION = 'Regression',
    UNIT = 'Unit',
    SMOKE = 'Smoke',
}

export class TestingStage extends cdk.Stage {


    constructor(scope: Construct, id: string, props: MyProps) {
        super(scope, id, props);

        new LambdaStack(this, 'LambdaStack', {
            removalPolicy: props.removalPolicy,
        });

    }
}