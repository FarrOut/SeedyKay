import {Duration, RemovalPolicy, Stack, StackProps} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as codedeploy from 'aws-cdk-lib/aws-codedeploy';
import * as lambda_ from 'aws-cdk-lib/aws-lambda';
import {Alias} from 'aws-cdk-lib/aws-lambda';

export class SandboxStack extends Stack {
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
            currentVersionOptions: {
                removalPolicy: RemovalPolicy.RETAIN, // retain old versions
                retryAttempts: 1,                   // async retry attempts
            },
            environment: {
                'CodeVersionString': chaos_theory,
            },
            // To fake a change for every deployment.
            // Thanks to https://github.com/aws/aws-cdk/issues/5334#issuecomment-562981777
            description: `Generated on: ${chaos_theory}`,
        });

        const version = fn.currentVersion // Blue Version

        const alias = new Alias(this, 'MyAlias', {
            aliasName: 'live',
            version: version,
        });


        const config = new codedeploy.CustomLambdaDeploymentConfig(this, 'CustomConfig', {
            type: codedeploy.CustomLambdaDeploymentConfigType.CANARY,
            interval: Duration.minutes(1),
            percentage: 5,
        });

        const application = new codedeploy.LambdaApplication(this, "MyApp", {
            applicationName: `MyApplication`
        });

        const deploymentGroup = new codedeploy.LambdaDeploymentGroup(this, 'BlueGreenDeployment', {
            application,
            alias: alias,
            deploymentConfig: config,
        });
    }
}
