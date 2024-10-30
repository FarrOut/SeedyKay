from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy,
)
from constructs import Construct

from motley.components.CICD.appconfig_nestedstack import AppConfigNestedStack
from motley.components.analytics.canary_nestedstack import CanaryNestedStack
from motley.components.analytics.forecast_stack import ForecastStack


class AppConfigStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        AppConfigNestedStack(
            self,
            "AppConfigNestedStack",
            removal_policy=removal_policy,
        )
