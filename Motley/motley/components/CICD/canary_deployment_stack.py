from aws_cdk import (
    # Duration,
    Stack, CfnOutput,
    RemovalPolicy, aws_ec2 as ec2,
)
from constructs import Construct

from motley.CICD.codedeploy_stack import CodeDeployStack
from Motley.motley.components.networking.application_load_balancer_nestedstack import LoadBalancerStack
from motley.computing.autoscaling_nestedstack import AutoScalingNestedStack


class CanaryDeploymentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, removal_policy: RemovalPolicy, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lb = LoadBalancerStack(
            self,
            "LoadBalancerStack",
            removal_policy=removal_policy,            
            vpc=vpc,
        )
        CfnOutput(self, "LoadBalancerDnsName", value=lb.alb.load_balancer_dns_name, description='The DNS name of this load balancer.')        

        asg = AutoScalingNestedStack(
            self,
            "AutoScalingStack",
            removal_policy=RemovalPolicy.DESTROY,
            vpc=vpc,
            key_name=self.node.try_get_context("key_name"),
            whitelisted_peer=ec2.Peer.prefix_list(self.node.try_get_context("peers")),            
        )

        codedeploy = CodeDeployStack(
            self,
            "CodeDeployStack",
            removal_policy=removal_policy,
            asg=asg.asg,
            load_balancer=lb.lb,
        )
        CfnOutput(self, "DeploymentGroupName", value=codedeploy.deployment_group.deployment_group_name, description="The name of the Deployment Group.")
        CfnOutput(self, "DeploymentGroupArn", value=codedeploy.deployment_group.deployment_group_arn, description="The ARN of the Deployment Group.")        