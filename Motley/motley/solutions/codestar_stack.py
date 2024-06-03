from aws_cdk import (
    # Duration,
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
    CfnParameter,
    aws_route53 as r53,
    CfnOutput,
    CfnTag,
    aws_route53profiles as route53profiles,
)
from constructs import Construct
from motley.components.CICD.codepipeline_stack import CodePipelineStack
from motley.components.CICD.codestar_notifications_nest import CodeStarNotificationsNest
from motley.components.networking.r53_profile_nest import Route53ProfileNest


class CodeStarStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc = None,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = CodePipelineStack(self, "CodePipelineStack").pipeline

        CodeStarNotificationsNest(
            self,
            "CodeStarNotificationsNest",
            pipeline=pipeline,
            removal_policy=removal_policy,
        )
