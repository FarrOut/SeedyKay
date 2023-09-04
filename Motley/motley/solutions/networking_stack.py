from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    RemovalPolicy,
)
from constructs import Construct
from motley.components.networking.elb_stack import ElbStack
from motley.components.networking.vpc_stack import VpcNestedStack


class NetworkingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        net = VpcNestedStack(self, "VpcStack", removal_policy=removal_policy)
        self.vpc = net.vpc

        # elb = ElbStack(self, "ElbStack", vpc=net.vpc, removal_policy=removal_policy)
