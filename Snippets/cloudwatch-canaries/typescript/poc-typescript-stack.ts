import * as cdk from '@aws-cdk/core';
import { CfnCanary, Canary, Runtime, Code, Test } from '@aws-cdk/aws-synthetics';
import * as s3 from '@aws-cdk/aws-s3';
import * as iam from '@aws-cdk/aws-iam';
import * as fs from 'fs';

export class PocTypescriptStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    var script_ = fs.readFileSync('canaries/pageLoadBlueprint.py', 'utf8');

    const role = new iam.Role(this, 'MyRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
    });

    const bucket_ = new s3.Bucket(this, 'MyFirstBucket');

    // L1 Resource
    const canaryL1 = new CfnCanary(this, 'typescript-tweetie', {
      name: 'TypescriptTweetie',
      runtimeVersion: 'syn-python-selenium-1.0',
      artifactS3Location: 's3://' + bucket_.bucketName,
      executionRoleArn: role.roleArn,
      schedule: new CfnCanary.ScheduleProperty({ expression: 'rate(1 minute)' }),
      code: new CfnCanary.CodeProperty({ script: script_, handler: 'custom.handler' }),
      startCanaryAfterCreation: true
    })

  }
}
