from aws_cdk import (
    Duration,
    NestedStack,
    aws_servicediscovery as servicediscovery,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecr as ecr,
    aws_appconfig as appconfig,
    aws_ec2 as ec2,
    CfnOutput,
    Fn,
    RemovalPolicy,
)
from aws_cdk.aws_ecs import ContainerImage, RepositoryImage
from aws_cdk.aws_secretsmanager import ISecret
from aws_cdk.aws_sns import Topic
from constructs import Construct
import json


class AppConfigNestedStack(NestedStack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an AppConfig Application
        app = appconfig.Application(
            self,
            "MyApplication",
            description="My AppConfig Application",
        )
        app.apply_removal_policy(removal_policy)

        # Create an AppConfig Environment
        environment = appconfig.Environment(
            self,
            "MyEnvironment",
            application=app,
            description="My AppConfig Environment",
        )
        environment.apply_removal_policy(removal_policy)

        # Create a Hosted Configuration Version
        content = {
            "flags": {"ui_refresh": {"name": "UI Refresh"}},
            "values": {
                "ui_refresh": {
                    "enabled": True,
                    "attributeValues": {"dark_mode_support": False},
                }
            },
            "version": "1",
        }
        appconfig.HostedConfiguration(
            self,
            "MyHostedConfiguration",
            application=app,
            content=appconfig.ConfigurationContent.from_inline_json(
                json.dumps(content)
            ),
            type=appconfig.ConfigurationType.FEATURE_FLAGS,
        )

        # Create a Deployment Strategy
        deployment_strategy = appconfig.DeploymentStrategy(
            self,
            "MyDeploymentStrategy",
            description="My AppConfig Deployment Strategy",
            rollout_strategy=appconfig.RolloutStrategy.linear(
                growth_factor=20,
                deployment_duration=Duration.minutes(30),
                final_bake_time=Duration.minutes(30),
            ),
        )
        deployment_strategy.apply_removal_policy(removal_policy)
