import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as iam from '@aws-cdk/aws-iam';
import * as destinations from '@aws-cdk/aws-lambda-destinations';
import * as s3 from '@aws-cdk/aws-s3';
import * as sqs from '@aws-cdk/aws-sqs';
import * as sns from '@aws-cdk/aws-sns';
import * as events from '@aws-cdk/aws-events';
import * as targets from '@aws-cdk/aws-events-targets';
import * as logs from '@aws-cdk/aws-logs';
import * as s3n from '@aws-cdk/aws-s3-notifications';
import fs = require('fs');

export class EventBridgeStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // =============================
    // S3
    // =============================
    const bucket = new s3.Bucket(this, 'MyBucket', {
      encryption: s3.BucketEncryption.KMS_MANAGED,
      publicReadAccess: false,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });
    new cdk.CfnOutput(this, 'BucketName', {
      description: 'Bucket',
      value: bucket.bucketName
    })

    // =============================
    // SNS
    // =============================
    const good_topic = new sns.Topic(this, 'GoodTopic', {
      displayName: 'Successful invocations'
    });
    const bad_topic = new sns.Topic(this, 'BadTopic', {
      displayName: 'Failed invocations'
    });

    // =============================
    // Lambda
    // =============================
    const func = new lambda.Function(this, 'MyFunction', {
      runtime: lambda.Runtime.NODEJS_12_X,            // execution environment
      code: lambda.Code.fromInline(`exports.handler = handler.toString()`),
      onFailure: new destinations.SnsDestination(bad_topic),
      onSuccess: new destinations.SnsDestination(good_topic),
      handler: 'index.handler',
    });

    new cdk.CfnOutput(this, 'Lambda Function', {
      description: 'My Lambda function.',
      value: func.functionArn
    })

// ====----====----====----====----====----====----====----====----====----====----

//   A solution using AWS EventBridge

// For more info see:
// @aws-cdk/aws-events module
// https://docs.aws.amazon.com/cdk/api/latest/docs/aws-events-readme.html

// What Is Amazon EventBridge?
// EventBridge was formerly called Amazon CloudWatch Events. Amazon EventBridge is a serverless event bus service that you can use to connect your applications with data from a variety of sources. EventBridge delivers a stream of real-time data from your applications, software as a service (SaaS) applications, and AWS services to targets such as AWS Lambda functions, HTTP invocation endpoints using API destinations, or event buses in other AWS accounts.

// https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html
// ====----====----====----====----====----====----====----====----====----====----

    // =============================
    // EventBus
    // =============================
    const rule = bucket.onCloudTrailWriteObject('onWriteBucketRule', {
      description: 'Trigger when object(s) are written.',
    });

    // Event retry policy and using dead-letter queues
    // https://docs.aws.amazon.com/cdk/api/latest/docs/aws-events-targets-readme.html#event-retry-policy-and-using-dead-letter-queues
    const queue = new sqs.Queue(this, 'Queue');

    // Invoke a Lambda function
    // https://docs.aws.amazon.com/cdk/api/latest/docs/aws-events-targets-readme.html#log-an-event-into-a-loggroup
    rule.addTarget(new targets.LambdaFunction(func, {
      deadLetterQueue: queue, // Optional: add a dead letter queue
      maxEventAge: cdk.Duration.minutes(5), // Otional: set the maxEventAge retry policy
      retryAttempts: 2, // Optional: set the max number of retry attempts
    }));

    // allow the Event Rule to invoke the Lambda function
    targets.addLambdaPermission(rule, func);

    // Log an event into a LogGroup
    // https://docs.aws.amazon.com/cdk/api/latest/docs/aws-events-targets-readme.html#log-an-event-into-a-loggroup
    const eventBridgeLogGroup = new logs.LogGroup(this, 'EventBridgeLogGroup', {
      retention: logs.RetentionDays.ONE_WEEK,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
    rule.addTarget(new targets.CloudWatchLogGroup(eventBridgeLogGroup));

  }
}
