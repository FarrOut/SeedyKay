from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_kms as kms,
    aws_lambda as lambda_,
    aws_secretsmanager as secretsmanager, RemovalPolicy, SecretValue,
)
from aws_cdk.aws_iam import ManagedPolicy, CompositePrincipal, ServicePrincipal
from aws_cdk.aws_lambda import Runtime, Code
from aws_cdk.aws_secretsmanager import Secret
from constructs import Construct


class LabStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        managed_policy_arn = ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')

        role = iam.Role(self, "Role",
                        assumed_by=CompositePrincipal(ServicePrincipal("lambda.amazonaws.com")),
                        # custom description if desired
                        description="This is a custom role...",
                        managed_policies=[managed_policy_arn],
                        )

        key = kms.Key(self, "MyKey")
        secret = Secret(self, "Secret",
                                       encryption_key=key,
                                       removal_policy=RemovalPolicy.DESTROY,
                                       secret_string_value=SecretValue.unsafe_plain_text('TopsyKretts'),
                                       )
        secret.grant_read(role)

        fn = lambda_.Function(self, "lambda_function",
                              runtime=Runtime.PYTHON_3_9,
                              handler="script.handler",
                              role=role,
                              environment={'secret_token': secret.secret_name},
                              environment_encryption=key,
                              code=Code.from_asset("./assets"))
