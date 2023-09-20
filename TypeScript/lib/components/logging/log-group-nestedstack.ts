import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as logs from 'aws-cdk-lib/aws-logs';

interface MyStackProps extends cdk.StackProps {
    removalPolicy: cdk.RemovalPolicy,
    retention: logs.RetentionDays,
}

export class LogGroupNestedStack extends cdk.NestedStack {

    public readonly logGroup: logs.ILogGroup;

    constructor(scope: Construct, id: string, props?: MyStackProps) {
        super(scope, id, props);

        this.logGroup = new logs.LogGroup(this, `PipelinesLogGroup`, {
            retention: props?.retention,
            removalPolicy: props?.removalPolicy,
        })

        new cdk.CfnOutput(this, 'LogGroupArn', {
            value: this.logGroup.logGroupArn,
            description: 'The ARN of this log group.', // Optional
        });
        new cdk.CfnOutput(this, 'LogGroupName', {
            value: this.logGroup.logGroupName,
            description: 'The name of this log group.', // Optional
        });
    }
}