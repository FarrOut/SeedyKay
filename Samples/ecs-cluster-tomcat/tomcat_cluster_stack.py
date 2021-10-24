from aws_cdk import (core as cdk,
                     aws_ecs as ecs,
                     aws_ec2 as ec2,
                     )

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class TomcatClusterStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC")

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "Cluster",
                              vpc=vpc
                              )

        # Add capacity to it
        cluster.add_capacity("DefaultAutoScalingGroupCapacity",
                             instance_type=ec2.InstanceType("t3.small"),
                             desired_capacity=3
                             )

        task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
        task_definition.add_container("DefaultContainer",
                                      image=ecs.ContainerImage.from_registry("tomcat"),
                                      memory_limit_mib=512
                                      )

        # Instantiate an Amazon ECS Service
        ecs_service = ecs.Ec2Service(self, "Service",
                                     cluster=cluster,
                                     task_definition=task_definition
                                     )
