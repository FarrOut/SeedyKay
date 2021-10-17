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

export class EventNotificationStack extends cdk.Stack {
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

    // Forward S3 Bucket notifications to Lambda
    bucket.addEventNotification(s3.EventType.OBJECT_CREATED, new s3n.LambdaDestination(func));
  }
}
