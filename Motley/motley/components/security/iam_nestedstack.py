from aws_cdk import (
    # Duration,
    NestedStack, RemovalPolicy, CfnOutput,aws_iam as iam,
)
from aws_cdk.aws_kms import Key

from constructs import Construct


class IamNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


