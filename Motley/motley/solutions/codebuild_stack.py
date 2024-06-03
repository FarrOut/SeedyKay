from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    RemovalPolicy,
)
from constructs import Construct
from motley.components.CICD.codebuild_nest import CodeBuildNest


class CodeBuildStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc = None,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cb = CodeBuildNest(
            self,
            "CodeBuildNest",
            vpc=vpc,
            subnet_id="subnet-00371b26ee7f7d4b6",
            removal_policy=removal_policy,
        )
