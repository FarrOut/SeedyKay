from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ec2 as ec2,
    aws_efs as efs, aws_ecs_patterns as ecs_patterns, aws_elasticloadbalancingv2 as elbv2,
    aws_ecs as ecs,
    CfnOutput,
    RemovalPolicy,
)
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_logs import LogGroup, RetentionDays
from constructs import Construct


class ApplicationLoadBalancedFargateServiceNestedStack(NestedStack):
    def __init__(
            self, scope: Construct, construct_id: str,
            cluster: ecs.ICluster,
            load_balancer: elbv2.IApplicationLoadBalancer,
            task_definition: ecs.FargateTaskDefinition,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.service = (
            ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
                                                               cluster=cluster,
                                                               load_balancer=load_balancer,
                                                               task_definition=task_definition,
                                                               ))

        CfnOutput(self, 'ClusterArn', value=self.service.cluster.cluster_arn,
                  description='The Amazon Resource Name (ARN) that identifies the cluster.')
        CfnOutput(self, 'ClusterName', value=self.service.cluster.cluster_name,
                  description='The name of the cluster.')
        CfnOutput(self, 'TargetGroup', value=self.service.target_group.target_group_arn,
                  description='The ARN of the target group.')        
