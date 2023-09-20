import {NestedStack} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as lambda_ from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as cdk from 'aws-cdk-lib';

interface MyProps {
    LogGroup?: logs.ILogGroup,
    removalPolicy: cdk.RemovalPolicy,
}

export class AlwaysUpdatingLambdaFunctionStack extends NestedStack {

    public readonly function: lambda_.IFunction;

    constructor(scope: Construct, id: string, props: MyProps) {
        super(scope, id, props);

        const lambdaRole = new iam.Role(this, 'Role', {
            assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
            description: 'Example role...',
        });
        lambdaRole.applyRemovalPolicy(props.removalPolicy)

        // Our programmer's trick to introduce randomness.
        let chaos_theory = new Date().toTimeString()

        this.function = new lambda_.Function(this, 'MyFunction', {
            runtime: lambda_.Runtime.NODEJS_18_X,
            handler: 'index.handler',
            code: lambda_.Code.fromInline(`exports.handler = handler.toString() //`),
            role: lambdaRole,
            environment: {
                // 'CodeVersionString': chaos_theory,
                'Stack': this.stackName,
            },
            // To fake a change for every deployment.
            // Thanks to https://github.com/aws/aws-cdk/issues/5334#issuecomment-562981777
            description: `Generated on: ${chaos_theory}`,
        });
        this.function.applyRemovalPolicy(props.removalPolicy)
    }
}
