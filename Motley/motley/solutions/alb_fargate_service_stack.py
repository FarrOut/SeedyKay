from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, aws_ec2 as ec2, aws_sns as sns, Duration, aws_ec2 as ec2, aws_ecs_patterns as ecs_patterns, aws_ecs as ecs, CfnOutput,
)
from constructs import Construct
from motley.components.analytics.cloudwatch_dashboard_nestedstack import CloudWatchDashboardNestedStack
from motley.components.analytics.cloudwatch_lambda_alarms_nestedstack import CloudWatchLambdaAlarmsNestedStack
from motley.components.networking.vpc_stack import VpcNestedStack
from motley.computing.lambda_nestedstack import LambdaNestedStack
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from motley.components.containerization.ecs_fargate_taskdefinition_nestedstack import EcsFargateTaskDefinitionNestedStack
from motley.components.containerization.ecs_nestedstack import EcsNestedStack
from aws_cdk.aws_ecs import ContainerImage


class AlbFargateServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 vpc_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 #  vpc: ec2.IVpc = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # if vpc is None:
        #     net = VpcNestedStack(
        #         self, "VpcStack", removal_policy=removal_policy)
        #     vpc = net.vpc

        vpc = ec2.Vpc.from_lookup(self, "Vpc", vpc_id=vpc_id)
        subnet = ec2.Subnet(self, 'MySubnet', vpc_id=vpc.vpc_id,
                            availability_zone=f'{self.region}c',
                            cidr_block='10.0.123.0/24',)
        subnet_selection = ec2.SubnetSelection(
            subnets=[ec2.Subnet.from_subnet_id(
                self, "subnet", subnet.subnet_id)]
        )

        ecs = EcsNestedStack(self, "EcsStack", vpc=vpc, removal_policy=removal_policy,
                             container_image=ContainerImage.from_registry("amazon/amazon-ecs-sample"))
        self.cluster = ecs.cluster

        CfnOutput(self, 'ClusterArn', value=self.cluster.cluster_arn,
                  description='The Amazon Resource Name (ARN) that identifies the cluster.')
        CfnOutput(self, 'ClusterName', value=self.cluster.cluster_name,
                  description='The name of the cluster.')

        task_definition = EcsFargateTaskDefinitionNestedStack(
            self, 'EcsFargateTaskDefinitionNestedStack').task_definition

        ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
                                                           cluster=self.cluster,
                                                           memory_limit_mib=1024,
                                                           cpu=512,
                                                           task_definition=task_definition, task_subnets=subnet_selection,
                                                           )
