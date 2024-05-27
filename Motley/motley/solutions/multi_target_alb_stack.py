from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2, aws_ecs_patterns as ecs_patterns, aws_ecs as ecs, aws_elasticloadbalancingv2 as elbv2,
    RemovalPolicy, CfnOutput, )
from aws_cdk.aws_ecs import ContainerImage
from constructs import Construct
from motley.components.containerization.ecs_fargate_taskdefinition_nestedstack import EcsFargateTaskDefinitionNestedStack
from motley.components.networking.application_load_balancer_nestedstack import LoadBalancerNestedStack
from motley.components.containerization.ecs_alb_fargate_service_nestedstack import ApplicationLoadBalancedFargateServiceNestedStack

from motley.components.containerization.ecs_nestedstack import EcsNestedStack


class MultiTargetAlbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 vpc: ec2.IVpc = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecs = EcsNestedStack(self, "EcsStack", vpc=vpc, removal_policy=removal_policy,
                             container_image=ContainerImage.from_registry("amazon/amazon-ecs-sample"))
        self.cluster = ecs.cluster

        CfnOutput(self, 'ClusterArn', value=self.cluster.cluster_arn,
                  description='The Amazon Resource Name (ARN) that identifies the cluster.')
        CfnOutput(self, 'ClusterName', value=self.cluster.cluster_name,
                  description='The name of the cluster.')

        load_balancer = LoadBalancerNestedStack(self, 'LoadBalancerNestedStack',
                                                internet_facing=True,
                                                vpc=vpc,
                                                removal_policy=removal_policy).alb

        CfnOutput(self, "LoadBalancerArn", value=load_balancer.load_balancer_arn,
                  description='The ARN of this load balancer.')

        task_definition = EcsFargateTaskDefinitionNestedStack(
            self, 'EcsFargateTaskDefinitionNestedStack').task_definition

        load_balanced_fargate_service = ApplicationLoadBalancedFargateServiceNestedStack(self, 'ApplicationLoadBalancedFargateServiceNestedStack',
                                                                                         cluster=self.cluster,
                                                                                         load_balancer=load_balancer,
                                                                                         task_definition=task_definition,
                                                                                         )
                                                                          
