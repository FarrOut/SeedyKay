from aws_cdk import (
    # Duration,
    NestedStack, aws_cloudwatch as cloudwatch, aws_iot as iot, aws_iam as iam,
    RemovalPolicy, CfnOutput, Tags, )
from constructs import Construct

from motley.components.iot.iot_logging_nestedstack import IoTloggingNestedStack
from motley.components.iot.iot_rules_nestedstack import IoTRulesNestedStack
from motley.computing.lambda_nestedstack import LambdaNestedStack


class IoTNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        logging_role = iam.Role(self, "IoTloggingRole",
                                assumed_by=iam.ServicePrincipal(
                                    "iot.amazonaws.com"),
                                description="The role used for the log."
                                )

        logging = IoTloggingNestedStack(self, 'IoTloggingNestedStack',
                                        removal_policy=removal_policy,
                                        account_id=self.account,
                                        role=logging_role,
                                        )

        function = LambdaNestedStack(self, 'LambdaNestedStack',).function


        rules = IoTRulesNestedStack(self, 'IoTRulesNestedStack',
                               removal_policy=removal_policy,   
                               function=function,  
        )