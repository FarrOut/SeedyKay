from aws_cdk import (
    # Duration,
    NestedStack,
    CfnTag,
    CfnOutput,
    aws_iam as iam,
    aws_codebuild as codebuild,
    aws_ec2 as ec2,
    custom_resources as cr,
    Duration,
    aws_lambda as lambda_,
    aws_logs as logs,
    Lazy,
    aws_iam as iam,
    RemovalPolicy,
)
from constructs import Construct
from datetime import datetime


class CodeBuildUpdater(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        parameters: dict,
        service_role: iam.IRole,
        removal_policy: RemovalPolicy = RemovalPolicy.DESTROY,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.log_group = logs.LogGroup(
            self,
            "LogGroup",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=removal_policy,
        )
        CfnOutput(
            self,
            "LogGroupArn",
            description="The ARN of this log group.",
            value=self.log_group.log_group_arn,
        )
        CfnOutput(
            self,
            "LogGroupName",
            description="The name of this log group.",
            value=self.log_group.log_group_name,
        )

        custom_resource = cr.AwsCustomResource(
            self,
            "UpdateFleet",
            log_group=self.log_group,
            role=service_role,
            on_update=cr.AwsSdkCall(  # will also be called for a CREATE event
                service="codebuild",
                action="UpdateFleet",
                parameters=parameters,
                physical_resource_id=cr.PhysicalResourceId.of(f"{datetime.now()}"),
            ),
            policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE
            ),
            install_latest_aws_sdk=False,
            timeout=Duration.seconds(5),
            removal_policy=removal_policy,
        )

        # Use the value in another construct with
        # self.response = custom_resource.get_response_field("fleet.status.message")
