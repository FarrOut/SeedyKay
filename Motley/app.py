#!/usr/bin/env python3
import os

import boto3
from aws_cdk import RemovalPolicy, App, Environment
from aws_cdk.aws_secretsmanager import Secret

from motley.components.security.waf_cloudfront_stack import WafCloudFrontStack
from motley.solutions.autoscaling_stack import AutoscalingStack
from motley.solutions.networking_stack import NetworkingStack
from motley.solutions.analytics_stack import AnalyticsStack
from motley.solutions.container_stack import ContainerStack

from motley.solutions.eks_stack import EksStack
from motley.solutions.security_stack import SecurityStack

secretsmanager_ = boto3.client("secretsmanager")

app = App()
peers = app.node.try_get_context("peers")
app_name = "motley"

default_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
africa_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='af-south-1')
euro_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='eu-central-1')

cross_account_a = app.node.try_get_context("cross_account_a")
cross_account_b = app.node.try_get_context("cross_account_b")

waf_stack = WafCloudFrontStack(app, "WafCloudFrontStack", removal_policy=RemovalPolicy.DESTROY, env=Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"), region='us-east-1'
), )

net = NetworkingStack(
    app,
    "NetworkingStack",
    waf=waf_stack.waf,
    removal_policy=RemovalPolicy.DESTROY,
    cross_region_references=True,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

analytics = AnalyticsStack(
    app,
    "AnalyticsStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

security = SecurityStack(
    app,
    "SecurityStack",
    removal_policy=RemovalPolicy.DESTROY,
    env=euro_env,
)

containers = ContainerStack(
    app,
    "ContainerStack",
    # vpc=net.vpc,
    image_name='farrout/reponderous:latest',
    secret_arn=security.secret.secret_full_arn,
    removal_policy=RemovalPolicy.DESTROY,
    env=africa_env,
    cross_region_references=True,
)

eks = EksStack(
    app,
    "EksStack",
    vpc=net.vpc,
    eks_version='1.24',
    removal_policy=RemovalPolicy.DESTROY,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

# canary_deployment = CanaryDeploymentStack(
#     app,
#     "CanaryDeploymentStack",
#     removal_policy=RemovalPolicy.DESTROY,
#     vpc=net.vpc,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

autoscaling = AutoscalingStack(
    app,
    "AutoscalingStack",
    removal_policy=RemovalPolicy.DESTROY,
    env=default_env,
)

app.synth()
