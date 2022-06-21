import {RemovalPolicy, Stack, StackProps} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as lambda_ from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';

export class AlwaysUpdatingLambdaFunctionStack extends Stack {
    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        const lambdaRole = new iam.Role(this, 'Role', {
            assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
            description: 'Example role...',
        });

        // Our programmer's trick to introduce randomness.
        let chaos_theory = new Date().toTimeString()

        const fn = new lambda_.Function(this, 'MyFunction', {
            runtime: lambda_.Runtime.NODEJS_14_X,
            handler: 'index.handler',
            code: lambda_.Code.fromInline(`exports.handler = handler.toString() //`),
            role: lambdaRole,
            environment: {
                'CodeVersionString': chaos_theory,
            },
            // To fake a change for every deployment.
            // Thanks to https://github.com/aws/aws-cdk/issues/5334#issuecomment-562981777
            description: `Generated on: ${chaos_theory}`,
        });
    }
}
