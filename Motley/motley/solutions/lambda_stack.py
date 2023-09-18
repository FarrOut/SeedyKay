from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_ecs import ContainerImage
from constructs import Construct
from motley.components.networking.vpc_stack import VpcNestedStack

from motley.computing.lambda_nestedstack import LambdaNestedStack
from motley.components.storage.filesystems.efs_nestedstack import EfsNestedStack


class LambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        net = VpcNestedStack(self, "VpcStack", removal_policy=removal_policy)
        vpc = net.vpc

        self.efs = EfsNestedStack(self, "EfsNestedStack", removal_policy=removal_policy, vpc=vpc,)

        self.lambda_ = LambdaNestedStack(self, "LambdaNestedStack", file_system=self.efs.file_system, vpc=vpc,removal_policy=removal_policy)
