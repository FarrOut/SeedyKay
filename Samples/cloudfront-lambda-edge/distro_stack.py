from aws_cdk import (core as cdk,
                     aws_cloudfront as cloudfront,
                     aws_lambda as lambda_,
                     aws_s3 as s3,
                     aws_cloudfront_origins as origins,
                     aws_stepfunctions as stepfunctions,
                     aws_stepfunctions_tasks as stepfunctions_tasks,
                     )

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk.aws_cloudfront import BehaviorOptions, LambdaEdgeEventType
from aws_cdk.aws_lambda import Runtime, Code, Version


class DistroStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        edge_function_arn = 'arn:aws:lambda:us-east-1:xxxxxxxx:function:EdgeStack-lambdafunction:1'
        cdk.CfnOutput(self, 'CurrentEdgeVersion',
                      value=edge_function_arn,
                      description='Current version of Lambda@Edge function.',
                      )

        # The code that defines your stack goes here
        my_bucket = s3.Bucket(self, "myBucket")

        version = Version.from_version_arn(self, '40YearOldVersion',
                                           version_arn=edge_function_arn,
                                           )

        edge = cloudfront.EdgeLambda(
            event_type=LambdaEdgeEventType.VIEWER_REQUEST,
            function_version=version,
        )

        cloudfront.Distribution(self, "myDist",
                                default_behavior=BehaviorOptions(origin=origins.S3Origin(my_bucket),
                                                                 edge_lambdas=[edge])
                                )
