from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    CfnOutput, RemovalPolicy,
)
from aws_cdk.aws_eks import EndpointAccess
from aws_cdk.aws_iam import Role, ManagedPolicy, ServicePrincipal
from constructs import Construct
from motley.analytics.forecast_stack import ForecastStack

from motley.components.orchestration.eks import Eks


class AnalyticsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, 
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        forecast = ForecastStack(            self,    "ForecastStack",)

        
