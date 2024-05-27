from aws_cdk import (
    # Duration,
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_kms as kms,
)
from constructs import Construct
from motley.components.security.kms_nest import KmsNest
from motley.components.storage.databases.rds_nestedstack import RdsNestedStack
from motley.components.storage.databases.rds_tagged_nest import RdsTaggedNest


class KmsStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        KmsNest(self, "KmsNest", removal_policy=removal_policy)
