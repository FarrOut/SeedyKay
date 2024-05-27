from aws_cdk import (
    # Duration,
    aws_ec2 as ec2,
    Stack, RemovalPolicy,
)
from constructs import Construct

from motley.components.networking.vpc_stack import VpcNestedStack
from motley.computing.autoscaling_nestedstack import AutoScalingNestedStack


class AutoscalingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        net = VpcNestedStack(self, "VpcStack", removal_policy=removal_policy)
        vpc = net.vpc

        autoscaling = AutoScalingNestedStack(self, "AutoScalingNestedStack", vpc=vpc,
                                             whitelisted_peer=ec2.Peer.any_ipv4(), key_name=None,
                                             removal_policy=removal_policy)
