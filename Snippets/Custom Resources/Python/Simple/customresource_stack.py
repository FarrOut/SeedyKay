from aws_cdk import (
    # Duration,
    Stack,
    custom_resources as cr,
    aws_logs as logs,
    aws_lambda as lambda_,
    CustomResource
)
from aws_cdk.aws_iam import ManagedPolicy, Role, ServicePrincipal
from aws_cdk.aws_lambda import Runtime, Code
from constructs import Construct


class CustomResourceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
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
                              handler="script.main",
                              role=role,
                              code=Code.from_asset("./assets"))

        custom_provider = cr.Provider(self, "MyProvider",
                                      on_event_handler=fn,
                                      # is_complete_handler=fn,  # optional async "waiter"
                                      log_retention=logs.RetentionDays.ONE_DAY,
                                      # default is INFINITE
                                      )
        custom = CustomResource(self, "Resource1", service_token=custom_provider.service_token)
