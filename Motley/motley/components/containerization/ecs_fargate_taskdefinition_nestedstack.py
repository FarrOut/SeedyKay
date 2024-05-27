from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_ecs as ecs,
    CfnOutput,
    RemovalPolicy,
)
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_logs import LogGroup, RetentionDays
from constructs import Construct


class EcsFargateTaskDefinitionNestedStack(NestedStack):
    def __init__(
            self, scope: Construct, construct_id: str,
            removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.task_definition = ecs.FargateTaskDefinition(self, "TaskDef")

        self.task_definition.add_container("TaskAlpha",
                                           image=ecs.ContainerImage.from_registry(
                                               "amazon/amazon-ecs-sample"),
                                           port_mappings=[ecs.PortMapping(
                                               container_port=80)],
                                           )
        self.task_definition.add_container("TaskBravo",
                                           image=ecs.ContainerImage.from_registry(
                                               "amazon/amazon-ecs-sample"),
                                           port_mappings=[ecs.PortMapping(
                                               container_port=2046)],
                                           # ephemeral_storage_gib=22,
                                           )
        self.task_definition.add_container("TaskCharlie",
                                           image=ecs.ContainerImage.from_registry(
                                               "amazon/amazon-ecs-sample"),
                                           port_mappings=[ecs.PortMapping(
                                               container_port=53)],
                                           # ephemeral_storage_gib=23,
                                           )

        CfnOutput(self, "TaskDefinitionArn", value=self.task_definition.task_definition_arn,
                  description='The full Amazon Resource Name (ARN) of the task definition.')
