from aws_cdk import (
    # Duration,
    aws_ec2 as ec2,
    Stack, RemovalPolicy,
)
from constructs import Construct
from motley.components.networking.vpc_stack import VpcNestedStack
from motley.computing.windows_instance_stack import WindowsInstanceStack

from motley.components.analytics.canary_nestedstack import CanaryNestedStack
from motley.components.analytics.forecast_stack import ForecastStack


class WindowsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,                 
                 whitelisted_peer: ec2.IPeer,
                 key_name: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 vpc: ec2.IVpc = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if vpc is None:
            net = VpcNestedStack(self, "VpcStack", removal_policy=removal_policy)
            vpc = net.vpc

        WindowsInstanceStack(self, 'WindowsInstanceStack',
                             removal_policy=removal_policy,
                             vpc=vpc,
                             whitelisted_peer=whitelisted_peer,
                             key_name=key_name,
                             )
