from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, aws_kms as kms,
)
from constructs import Construct
from motley.components.storage.block.secure_s3_nestedstack import SecureS3NestedStack

from motley.components.analytics.canary_nestedstack import CanaryNestedStack
from motley.components.analytics.forecast_stack import ForecastStack


class S3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        key = kms.Key(self, "MyKey",
                      enable_key_rotation=True
                      )

        SecureS3NestedStack(self, 'SecureS3NestedStack',
                            removal_policy=removal_policy,
                            auto_delete_objects=True,
                            custom_kms_key=key,
                            )
