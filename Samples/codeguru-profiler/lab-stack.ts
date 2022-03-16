import {Duration, Stack, StackProps} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import {Code, LayerVersion} from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import {Effect, PolicyStatement} from 'aws-cdk-lib/aws-iam';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import {Rule, Schedule} from 'aws-cdk-lib/aws-events';
import {LambdaFunction} from 'aws-cdk-lib/aws-events-targets';
import {Bucket} from "aws-cdk-lib/aws-s3";


export class LabStack extends Stack {

    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        let region = Stack.of(this).region
        const CodeGuruLayer = LayerVersion.fromLayerVersionArn(this, "CodeGuruLayer",
            'arn:aws:lambda:' + region + ':157417159150:layer:AWSCodeGuruProfilerPythonAgentLambdaLayer:11',
        )

        const bucket = new Bucket(this, 'MyBucket');

        const fn = new lambda.Function(this, 'MyFunction', {
            runtime: lambda.Runtime.PYTHON_3_9,
            handler: 'sample-lambda-demo-app.lambda_handler',
            code: Code.fromAsset("./assets"),
            profiling: true,
            environment: {
                'AWS_LAMBDA_EXEC_WRAPPER': '/opt/codeguru_profiler_lambda_exec',
                'AWS_CODEGURU_PROFILER_TARGET_REGION': region,
                'S3_BUCKET': bucket.bucketName,
            },
            timeout: Duration.seconds(10),
            layers: [CodeGuruLayer],
        });
        bucket.grantReadWrite(fn)
        fn.addToRolePolicy(new PolicyStatement({
            resources: ['*'],
            effect: Effect.ALLOW,
            actions: ["s3:PutObject",
                "cloudwatch:PutMetricData"],
        }))

        fn.role?.addManagedPolicy(
            iam.ManagedPolicy.fromAwsManagedPolicyName(
                'AmazonCodeGuruProfilerAgentAccess',
            ),
        );

        const queue = new sqs.Queue(this, 'Queue');

        const rule = new Rule(this, 'ScheduleRule', {
            schedule: Schedule.rate(Duration.minutes(1)),
        });
        rule.addTarget(new LambdaFunction(fn, {
            deadLetterQueue: queue, // Optional: add a dead letter queue
            maxEventAge: Duration.minutes(1), // Optional: set the maxEventAge retry policy
            retryAttempts: 2, // Optional: set the max number of retry attempts
        }));
    }
}
