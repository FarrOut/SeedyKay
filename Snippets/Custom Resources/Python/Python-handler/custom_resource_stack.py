from aws_cdk import (
    Duration,
    custom_resources as cr,
    aws_logs as logs,
    aws_lambda as lambda_,
    aws_ec2 as ec2, CfnOutput, CfnTag, NestedStack, Size, RemovalPolicy, Tags, CustomResource
)
from aws_cdk.aws_iam import ManagedPolicy, Role, ServicePrincipal
from aws_cdk.aws_lambda import Runtime, Code
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct


class CustomResourceStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, tag_value: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        managed_policy_arn = ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')

        role = Role(self, "Role",
                    assumed_by=ServicePrincipal("lambda.amazonaws.com"),
                    # custom description if desired
                    description="This is a custom role...",
                    managed_policies=[managed_policy_arn],
                    )

        fn = lambda_.Function(self, "lambda_function",
                              runtime=Runtime.PYTHON_3_9,
                              handler="script.handler",
                              role=role,
                              log_retention=RetentionDays.ONE_DAY,
                              code=Code.from_asset("./assets"))

        custom_provider = cr.Provider(self, "MyProvider",
                                      on_event_handler=fn,
                                      # is_complete_handler=fn,  # optional async "waiter"
                                      log_retention=logs.RetentionDays.ONE_DAY,
                                      # total_timeout=Duration.minutes(2),
                                      )
        custom = CustomResource(self, "Resource1", service_token=custom_provider.service_token,
                                removal_policy=RemovalPolicy.DESTROY,
                                properties={
                                    # 'No1': 1,
                                    # 'No2': 2,
                                },
                                )