from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_ecs as ecs,aws_iam as iam,
    CfnOutput,
    RemovalPolicy,
)
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_logs import LogGroup, RetentionDays
from constructs import Construct


class EcsNestedStack(NestedStack):
    def __init__(
            self, scope: Construct, construct_id: str, vpc: ec2.Vpc, container_image: ContainerImage = None,
            task_role: iam.IRole = None,
            removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        container_port = 80

        self.cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        CfnOutput(self, 'ClusterArn', value=self.cluster.cluster_arn,
                  description='The Amazon Resource Name (ARN) that identifies the cluster.')
        CfnOutput(self, 'ClusterName', value=self.cluster.cluster_name,
                  description='The name of the cluster.')

        # file_system = efs.FileSystem(
        #     self,
        #     "MyEfsFileSystem",
        #     vpc=vpc,
        #     lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,
        #     # files are not transitioned to infrequent access (IA) storage by default
        #     performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
        #     out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS,
        #     removal_policy=removal_policy,
        # )
        # volume_one = ecs.Volume(
        #     name="SeaDrive",
        #     efs_volume_configuration=ecs.EfsVolumeConfiguration(
        #         file_system_id=file_system.file_system_id,
        #     ),
        # )

        self.task_def = ecs.FargateTaskDefinition(
            self,
            "TaskDef",
            memory_limit_mib=512,
            cpu=256,
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                cpu_architecture=ecs.CpuArchitecture.X86_64,
            ),
            # volumes=[volume_one],
            task_role=task_role,
        )

        security_group = ec2.SecurityGroup(self, "SecurityGroup", vpc=vpc, allow_all_outbound=True, )
        security_group.connections.allow_from_any_ipv4(ec2.Port.tcp(container_port))

        log_group = LogGroup(
            self,
            "LogGroup",
            retention=RetentionDays.ONE_WEEK,
            removal_policy=removal_policy,
        )

        if container_image is None:
            container_image = ContainerImage.from_registry("amazon/amazon-ecs-sample",)

        container_def = ecs.ContainerDefinition(
            self,
            "ContainerDef",
            task_definition=self.task_def,
            image=container_image,
            port_mappings=[
                ecs.PortMapping(container_port=container_port, protocol=ecs.Protocol.TCP)
            ],
            logging=ecs.AwsLogDriver(
                stream_prefix="EventDemo",
                mode=ecs.AwsLogDriverMode.NON_BLOCKING,
                log_group=log_group,
            ),
        )

        CfnOutput(
            self,
            "ContainerName",
            description="The name of this container.",
            value=container_def.container_name,
        )
        CfnOutput(
            self,
            "ContainerPort",
            description="The port the container will listen on.",
            value=str(container_def.container_port),
        )
        CfnOutput(
            self,
            "ContainerCpu",
            description="The number of cpu units reserved for the container.",
            value=str(container_def.cpu),
        )
        CfnOutput(
            self,
            "ContainerIsEssential",
            description="Specifies whether the container will be marked essential.",
            value=str(container_def.essential),
        )
        CfnOutput(
            self,
            "ContainerImageName",
            description="The name of the image referenced by this container.",
            value=container_def.image_name,
        )

        log_driver_config = container_def.log_driver_config
        if log_driver_config is not None:
            CfnOutput(
                self,
                "ContainerLogDriver",
                description="The log driver to use for the container.",
                value=str(log_driver_config.log_driver),
            )
            CfnOutput(
                self,
                "ContainerLogDriverOptions",
                description="The configuration options to send to the log driver.",
                value=str(log_driver_config.options),
            )
