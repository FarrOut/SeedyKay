from aws_cdk import (
    # Duration,
    NestedStack, aws_ec2 as ec2,
    RemovalPolicy,
)
from aws_cdk.aws_secretsmanager import ISecret, Secret
from constructs import Construct

from motley.components.containerization.ecr_image_nestedstack import EcrImageNestedStack
from motley.components.containerization.ecs_nestedstack import EcsNestedStack
from motley.components.networking.vpc_stack import VpcNestedStack


class ContainerStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, image_name: str, vpc: ec2.Vpc = None,
                 # secret: ISecret = None,
                 secret_arn: str = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        net = VpcNestedStack(self, "VpcStack", removal_policy=removal_policy)
        vpc = net.vpc

        ecr = EcrImageNestedStack(self, "EcrImageNestedStack", image_name=image_name,
                                  credentials=Secret.from_secret_complete_arn(self, "Secret", secret_arn),
                                  removal_policy=removal_policy)

        ecs = EcsNestedStack(self, "EcsStack", vpc=vpc, removal_policy=removal_policy,
                             container_image=ecr.image)
