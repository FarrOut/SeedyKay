import { Stack, StackProps, CfnOutput } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import iam = require('aws-cdk-lib/aws-iam');

export class RoleStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const lambdaRole = new iam.Role(this, 'Role', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      description: 'Example role...',
    });

    new CfnOutput(this, 'RoleArn', { value: lambdaRole.roleArn });

  }
}
