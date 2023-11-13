import jsii
from aws_cdk import (
    Duration,     aws_ec2 as ec2,
    aws_efs as efs,
    aws_ecs as ecs, aws_iam as iam,
    Stack, aws_ec2 as ec2, aws_ecs as ecs, aws_servicediscovery as servicediscovery,
    CfnOutput, RemovalPolicy, Tags, Aspects, IAspect,
)
from aws_cdk.aws_eks import EndpointAccess, KubernetesVersion, Nodegroup
from aws_cdk.aws_iam import Role, ManagedPolicy, ServicePrincipal
from constructs import Construct
from motley.solutions.container_stack import ContainerStack
from motley.components.containerization.ecs_nestedstack import EcsNestedStack
from motley.components.containerization.cloudmap_nestedstack import CloudMapNestedStack
from motley.components.containerization.ecr_docker_asset_nestedstack import EcrDockerAssetNestedStack
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_logs import LogGroup, RetentionDays
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

        container_port = 80

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        CfnOutput(self, 'ClusterArn', value=cluster.cluster_arn,
                  description='The Amazon Resource Name (ARN) that identifies the cluster.')
        CfnOutput(self, 'ClusterName', value=cluster.cluster_name,
                  description='The name of the cluster.')

        task_def = ecs.FargateTaskDefinition(
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

        security_group = ec2.SecurityGroup(
            self, "SecurityGroup", vpc=vpc, allow_all_outbound=True, )
        security_group.connections.allow_from_any_ipv4(
            ec2.Port.tcp(container_port))

        log_group = LogGroup(
            self,
            "LogGroup",
            retention=RetentionDays.ONE_WEEK,
            removal_policy=removal_policy,
        )

        container_def = ecs.ContainerDefinition(
            self,
            "ContainerDef",
            task_definition=task_def,
            image=ContainerImage.from_registry(
                "amazon/amazon-ecs-sample",),
            port_mappings=[
                ecs.PortMapping(container_port=container_port,
                                protocol=ecs.Protocol.TCP)
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

        fargate_service = ecs.FargateService(self, "FargateService",
                                     cluster=cluster,
                                     task_definition=task_def,
                                     assign_public_ip=True,
                                     desired_count=2,
                                     )

        namespace = servicediscovery.HttpNamespace(self, "MyNamespace",
                                                   name="MyHTTPNamespace"
                                                   )
        namespace.apply_removal_policy(removal_policy)

        cloudmap_service = namespace.create_service("Service",
                                                # health_check=servicediscovery.HealthCheckConfig(
                                                #     type=servicediscovery.HealthCheckType.HTTP,
                                                #     resource_path="/check"
                                                # ),
                                                custom_health_check=servicediscovery.HealthCheckCustomConfig(
                                                    failure_threshold=3,
                                                ),
                                                )
        cloudmap_service.apply_removal_policy(removal_policy)
        instance = cloudmap_service.register_non_ip_instance('NationalService', custom_attributes={
            "attribute": "custom"
        })
        instance.apply_removal_policy(removal_policy)

        CfnOutput(self, 'DiscoveryType', value=str(cloudmap_service.discovery_type),
                  description='The discovery type used by this service.')
        CfnOutput(self, 'DnsRecordType', value=str(cloudmap_service.dns_record_type),
                  description='The DnsRecordType used by the service.')
        CfnOutput(self, 'Namespace', value=str(cloudmap_service.namespace),
                  description='The namespace for the Cloudmap Service.')
        CfnOutput(self, 'RoutingPolicy', value=str(cloudmap_service.routing_policy),
                  description='The Routing Policy used by the service.')
        CfnOutput(self, 'ServiceArn', value=str(cloudmap_service.service_arn),
                  description='The Arn of the namespace that you want to use for DNS configuration.')
        CfnOutput(self, 'ServiceId', value=str(cloudmap_service.service_id),
                  description='The ID of the namespace that you want to use for DNS configuration.')
        CfnOutput(self, 'ServiceName', value=str(cloudmap_service.service_name),
                  description='A name for the Cloudmap Service.')

        fargate_service.associate_cloud_map_service(
            service=cloudmap_service,
        )
