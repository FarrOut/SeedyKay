from aws_cdk import (
    # Duration,
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling, RemovalPolicy,
    custom_resources as cr,
)
from constructs import Construct
from datetime import datetime


class ContainerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc, )

        asg = autoscaling.AutoScalingGroup(self, "ASG",
                                           vpc=vpc,
                                           instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3,
                                                                             ec2.InstanceSize.MEDIUM),
                                           machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
                                           min_capacity=1,
                                           max_capacity=3,
                                           )
        asg.role.apply_removal_policy(RemovalPolicy.DESTROY)

        capacity_provider = ecs.AsgCapacityProvider(self, "AsgCapacityProvider",
                                                    auto_scaling_group=asg,
                                                    enable_managed_termination_protection=True,
                                                    )
        cluster.add_asg_capacity_provider(capacity_provider)
        task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
        task_definition.add_container("web",
                                      image=ecs.ContainerImage.from_registry("tomcat"),
                                      memory_reservation_mib=512
                                      )

        service = ecs.Ec2Service(self, "EC2Service",
                                 cluster=cluster,
                                 task_definition=task_definition,
                                 capacity_provider_strategies=[ecs.CapacityProviderStrategy(
                                     capacity_provider=capacity_provider.capacity_provider_name,
                                     weight=1
                                 )
                                 ]
                                 )

        force_delete_asg = cr.AwsCustomResource(self, "ForceDeleteAsg",
                                                install_latest_aws_sdk=True,
                                                on_delete=cr.AwsSdkCall(
                                                    service="AutoScaling",
                                                    action="deleteAutoScalingGroup",
                                                    parameters={
                                                        "AutoScalingGroupName": asg.auto_scaling_group_name,
                                                        "ForceDelete": True
                                                    },
                                                    physical_resource_id=cr.PhysicalResourceId.of(
                                                        str(datetime.now()))),
                                                policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                                                    resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE
                                                )
                                                )
        force_delete_asg.node.add_dependency(asg)
