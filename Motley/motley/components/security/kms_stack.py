from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_kms import Key

from constructs import Construct


class KmsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        key = Key(self, "MyKey",
                  removal_policy=RemovalPolicy.DESTROY
                  )

        key.add_alias("alias/foo")
        key.add_alias("alias/bar")

        CfnOutput(self, 'KmsKeyId',
                  description='The ID of the key (the part that looks something like.',
                  value=key.key_id,
                  )
        CfnOutput(self, 'KmsKeyArn',
                  description='The ARN of the key.',
                  value=key.key_arn,
                  )
