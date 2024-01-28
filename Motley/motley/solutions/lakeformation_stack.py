from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy,
)
from constructs import Construct

from motley.components.analytics.lakeformation_nestedstack import LakeFormation


class LakeFormationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        LakeFormation(self, 'LakeFormationStack', removal_policy=removal_policy)
