import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import iam = require('aws-cdk-lib/aws-iam');
import lambda = require('aws-cdk-lib/aws-lambda');

export class FunctionStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const imported_role = iam.Role.fromRoleArn(this, 'importedRole',
      'arn:aws:iam::xxxxxxxxxxxxx:role/RoleStack-Role1ABCC5F0-1CAONSSGTHUZN',
    );

    const fn = new lambda.Function(this, 'MyFunction', {
      runtime: lambda.Runtime.NODEJS_14_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`exports.handler = handler.toString()`),
      role: imported_role,
    });
  }
}
