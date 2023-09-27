from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, aws_ec2 as ec2,
)
from constructs import Construct
from motley.computing.batch_nestedstack import BatchNestedStack
from motley.components.networking.vpc_stack import VpcNestedStack


class BatchStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 vpc: ec2.IVpc = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if vpc is None:
            net = VpcNestedStack(
                self, "VpcStack", removal_policy=removal_policy)
            vpc = net.vpc

        BatchNestedStack(self, 'BatchNestedStack', removal_policy=removal_policy,
                         vpc=vpc,
                         replace_compute_environment=False,
                         maxv_cpus=9,
                         )
