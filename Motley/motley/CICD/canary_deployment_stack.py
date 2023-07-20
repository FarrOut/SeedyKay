from aws_cdk import (
    # Duration,
    Stack,CfnOutput,
    aws_codepipeline as codepipeline,aws_cloudwatch as cloudwatch,
    aws_s3 as s3,aws_codedeploy as codedeploy,
    aws_s3_deployment as s3deploy, RemovalPolicy,aws_autoscaling as autoscaling,aws_iam as iam,aws_codecommit as codecommit,aws_ec2 as ec2,
)
from aws_cdk.aws_codepipeline import StageProps
from aws_cdk.aws_codepipeline_actions import CloudFormationDeployStackSetAction, StackSetTemplate, \
    StackSetDeploymentModel, StackInstances, \
    S3SourceAction, S3Trigger
from aws_cdk.aws_s3_deployment import BucketDeployment
from constructs import Construct

from motley.CICD.codedeploy_stack import CodeDeployStack
from motley.computing.autoscaling_stack import AutoScalingStack
from motley.networking.load_balancer_stack import LoadBalancerStack


class CanaryDeploymentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, removal_policy: RemovalPolicy, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lb = LoadBalancerStack(
            self,
            "LoadBalancerStack",
            removal_policy=removal_policy,            
            vpc=vpc,
        )
        CfnOutput(self, "LoadBalancerDnsName", value=lb.lb.load_balancer_dns_name, description='The DNS name of this load balancer.')        

        asg = AutoScalingStack(
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
        )
        CfnOutput(self, "DeploymentGroupName", value=codedeploy.deployment_group.deployment_group_name, description="The name of the Deployment Group.")
        CfnOutput(self, "DeploymentGroupArn", value=codedeploy.deployment_group.deployment_group_arn, description="The ARN of the Deployment Group.")        