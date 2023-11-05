import jsii
from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2, aws_ecs as ecs,
    CfnOutput, RemovalPolicy, Tags, Aspects, IAspect,
)
from aws_cdk.aws_eks import EndpointAccess, KubernetesVersion, Nodegroup
from aws_cdk.aws_iam import Role, ManagedPolicy, ServicePrincipal
from constructs import Construct
from motley.solutions.container_stack import ContainerStack
from motley.components.containerization.ecs_nestedstack import EcsNestedStack
from motley.components.containerization.cloudmap_nestedstack import CloudMapNestedStack
from motley.components.containerization.ecr_docker_asset_nestedstack import EcrDockerAssetNestedStack

from motley.components.networking.vpc_stack import VpcNestedStack
from motley.components.orchestration.eks import Eks
from motley.components.orchestration.mini_eks import MiniEks


class CloudMapStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if vpc is None:
            net = VpcNestedStack(
                self, "VpcStack", removal_policy=removal_policy)
            vpc = net.vpc

        task_role = Role(self, 'TaskRole', assumed_by=ServicePrincipal(
            'ecs-tasks.amazonaws.com'))
        task_role.apply_removal_policy(removal_policy)
        task_role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name(
            "service-role/AmazonECSTaskExecutionRolePolicy"))

        self.ecs = EcsNestedStack(
            self, "EcsStack", vpc=vpc, removal_policy=removal_policy, task_role=task_role,)

        service = ecs.FargateService(self, "Service",
                                     cluster=self.ecs.cluster,
                                     task_definition=self.ecs.task_def,
                                     assign_public_ip=True,
                                     desired_count=2,
                                     )

        cloudmap = CloudMapNestedStack(
            self, 'CloudMapNestedStack', removal_policy=removal_policy, vpc=vpc,)

        service.associate_cloud_map_service(
            service=cloudmap.service,
        )
