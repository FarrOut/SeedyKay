from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs, CfnOutput,
)
from aws_cdk.aws_ecs import AddCapacityOptions
from constructs import Construct


class EcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "Cluster",
                              vpc=vpc,

                              # https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/1469
                              capacity=AddCapacityOptions(instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3,
                                                                                            ec2.InstanceSize.MEDIUM)),
                              enable_fargate_capacity_providers=False,
                              )

        task_definition = ecs.FargateTaskDefinition(self, "TaskDef",

                                                    cpu=512,
                                                    memory_limit_mib=1024,

                                                    )
        task_definition.add_container("DefaultContainer",
                                      image=ecs.ContainerImage.from_registry("tomcat"),
                                      memory_limit_mib=1024
                                      )

        # Instantiate an Amazon ECS Service
        ecs_service = ecs.FargateService(self, "Service", cluster=cluster, task_definition=task_definition)

        CfnOutput(self, 'ServiceName',
                  value=ecs_service.service_name,
                  description='The name of the service.'
                  )
        CfnOutput(self, 'ServiceArn',
                  value=ecs_service.service_arn,
                  description='The Amazon Resource Name (ARN) of the service.'
                  )
