import jsii
from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    CfnOutput, RemovalPolicy, Tags, Aspects, IAspect,
)
from aws_cdk.aws_eks import EndpointAccess, KubernetesVersion, Nodegroup
from aws_cdk.aws_iam import Role, ManagedPolicy, ServicePrincipal
from constructs import Construct
from motley.components.containerization.ecr_docker_asset_nestedstack import EcrDockerAssetNestedStack

from motley.components.networking.vpc_stack import VpcNestedStack
from motley.components.orchestration.eks import Eks
from motley.components.orchestration.mini_eks import MiniEks


class EcrStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        EcrDockerAssetNestedStack(self, 'EcrDockerAssetNestedStack', removal_policy=removal_policy)