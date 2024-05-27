from aws_cdk import (
    # Duration,
    NestedStack,
    RemovalPolicy,
    CfnOutput,CfnParameter,
    aws_iam as iam,
)
from aws_cdk.aws_kms import Key

from constructs import Construct


class KmsNest(NestedStack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.key = Key(self, "MyKey", removal_policy=removal_policy)

        self.key.add_alias("alias/foo")
        self.key.add_alias("alias/bar")

        CfnOutput(
            self,
            "KmsKeyId",
            description="The ID of the key (the part that looks something like.",
            value=self.key.key_id,
        )
        CfnOutput(
            self,
            "KmsKeyArn",
            description="The ARN of the key.",
            value=self.key.key_arn,
        )

        account_param = CfnParameter(self, 'Account',)

        self.key.grant_admin(iam.AccountPrincipal(account_param.value_as_string))
        self.key.grant_decrypt(iam.ServicePrincipal("ec2.amazonaws.com"))
