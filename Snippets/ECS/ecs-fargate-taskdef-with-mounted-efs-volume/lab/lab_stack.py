from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs, RemovalPolicy,
)
from aws_cdk.aws_ecs import EfsVolumeConfiguration
from aws_cdk.aws_efs import FileSystem
from constructs import Construct


class LabStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, file_system: FileSystem, vpc: ec2.Vpc, security_group_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        volume = ecs.Volume(
            name="MyVolume",
            efs_volume_configuration=ecs.EfsVolumeConfiguration(
                file_system_id=file_system.file_system_id
            )
        )

        fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
                                                            memory_limit_mib=512,
                                                            cpu=256,
                                                            volumes=[volume],
                                                            )
        fargate_task_definition.apply_removal_policy(RemovalPolicy.DESTROY)

        container = fargate_task_definition.add_container("WebContainer",
                                                          # Use an image from DockerHub
                                                          image=ecs.ContainerImage.from_registry(
                                                              "amazon/amazon-ecs-sample")
                                                          )

        container_volume_mount_point = ecs.MountPoint(
            read_only=True,
            container_path="/var/www/html",
            source_volume=volume.name
        )
        container.add_mount_points(container_volume_mount_point)

        cluster = ecs.Cluster(self, "FargateCPCluster",
                              vpc=vpc,
                              enable_fargate_capacity_providers=True
                              )

        service = ecs.FargateService(self, "FargateService",
                                     cluster=cluster,
                                     task_definition=fargate_task_definition,
                                     capacity_provider_strategies=[ecs.CapacityProviderStrategy(
                                         capacity_provider="FARGATE_SPOT",
                                         weight=2
                                     ), ecs.CapacityProviderStrategy(
                                         capacity_provider="FARGATE",
                                         weight=1
                                     )
                                     ]
                                     )

        nfs_security_group = ec2.SecurityGroup.from_lookup_by_id(self, 'ImportedSecurityGroup',
                                                                 security_group_id=security_group_id,
                                                                 )

        fs = FileSystem.from_file_system_attributes(self, 'ImportedFileSystem',
                                                    file_system_id=file_system.file_system_id,
                                                    security_group=nfs_security_group,
                                                    )

        # https://docs.aws.amazon.com/efs/latest/ug/troubleshooting-efs-mounting.html#mount-hangs-fails-timeout
        fs.connections.allow_default_port_from(service)
