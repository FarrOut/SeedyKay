import os

from aws_cdk import (core as cdk,
                     aws_cloudfront as cloudfront,
                     aws_cloudfront_origins as origins,
                     aws_lambda as lambda_,
                     aws_s3 as s3,
                     aws_iam as iam,
                     aws_stepfunctions as stepfunctions,
                     )

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk.aws_cloudfront import BehaviorOptions, LambdaEdgeEventType
from aws_cdk.aws_iam import ManagedPolicy, CompositePrincipal, ServicePrincipal
from aws_cdk.aws_lambda import Runtime, Code


class EdgeStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        managed_policy_arn = ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')

        role = iam.Role(self, "Role",
                        assumed_by=CompositePrincipal(ServicePrincipal("lambda.amazonaws.com"),
                                                      ServicePrincipal("edgelambda.amazonaws.com")),
                        # custom description if desired
                        description="This is a custom role...",
                        managed_policies=[managed_policy_arn],
                        )

        fn = lambda_.Function(self, "lambda_function",
                              runtime=Runtime.PYTHON_3_8,
                              handler="script.main",
                              role=role,
                              code=Code.asset("./assets"))

        self.current_version = fn.current_version
        cdk.CfnOutput(self, 'CurrentEdgeVersion',
                      value=self.current_version.edge_arn,
                      description='Current version of Lambda@Edge function.',
                      )

        # edge = cloudfront.EdgeLambda(
        #     event_type=LambdaEdgeEventType.ORIGIN_REQUEST,
        #     function_version=version,
        # )

    # Using the property decorator
    @property
    def get_current_version(self) -> lambda_.IVersion:
        return self.current_version
