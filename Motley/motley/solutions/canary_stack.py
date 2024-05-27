from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy,
)
from constructs import Construct

from motley.components.analytics.canary_nestedstack import CanaryNestedStack
from motley.components.analytics.forecast_stack import ForecastStack


class CanaryStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        CanaryNestedStack(self, 'CanaryNestedStack',
                          removal_policy=removal_policy,
                          )
