import * as cdk from 'aws-cdk-lib';
import {CfnOutput, RemovalPolicy, SecretValue, Tags} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {Topic} from 'aws-cdk-lib/aws-sns';
import * as secretsmanager from "aws-cdk-lib/aws-secretsmanager";
import * as lambda_ from "aws-cdk-lib/aws-lambda";

export class SecretStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const secret = new secretsmanager.Secret(this, 'Secret', {
            removalPolicy: RemovalPolicy.DESTROY,
            secretStringValue: SecretValue.unsafePlainText('for your eyes only')
        })

        let secret_value = secret.secretValue.unsafeUnwrap()


        new CfnOutput(this, 'SecretName',
            {
                value: secret.secretName,
                description: 'The name of the secret.'
            }
        )

        new CfnOutput(this, 'SecretArn',
            {
                value: secret.secretArn,
                description: 'The ARN of the secret in AWS Secrets Manager.'
            }
        )


        /*
        Let's print the secret value out to demonstrate how it can be passed to other places.
         */
        new CfnOutput(this, 'SecretValueToken',
            {
                value: secret_value,
                description: 'The secret. Note: It is still the unresolved token at this stage.'
            }
        )

        /*
        Passing the resolved secret value to any resource, just to see it resolving."
         */
        const topic = new Topic(this, 'Topic', {})
        Tags.of(topic).add('Secret', secret_value)

        const fn = new lambda_.Function(this, 'Dysfunction', {
            runtime: lambda_.Runtime.NODEJS_18_X,
            handler: 'index.handler',
            code: lambda_.Code.fromInline(`exports.handler = handler.toString() //`),
            environment: {
                SECRET_VALUE: secret_value
            },
        });

        // Remember to grant our Lambda handler permission to retrieve our secret from inside the function!
        secret.grantRead(fn)

    }
}
