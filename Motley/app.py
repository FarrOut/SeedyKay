#!/usr/bin/env python3
import os

import boto3
from aws_cdk import (
    # Duration,
    aws_ec2 as ec2,
    RemovalPolicy, App, Environment,
)

from motley.solutions.multi_target_alb_stack import MultiTargetAlbStack
from motley.solutions.ssm_stack import SsmStack
from motley.solutions.events_stack import EventsStack
from motley.solutions.efs_stack import EfsStack
from motley.solutions.rds_stack import RdsStack

from motley.solutions.batch_stack import BatchStack
from motley.solutions.canary_stack import CanaryStack
from motley.solutions.certificate_manager_stack import CertificateManagerStack
from motley.solutions.eks_stack import EksStack
from motley.solutions.inspector_stack import InspectorStack
from motley.solutions.lambda_stack import LambdaStack
from motley.solutions.networking_stack import NetworkingStack
from motley.solutions.windows_stack import WindowsStack

secretsmanager_ = boto3.client("secretsmanager")

app = App()
peers = app.node.try_get_context("peers")
key_name = app.node.try_get_context("key_name")
app_name = "motley"

default_env = Environment(account=os.getenv(
    'CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
africa_env = Environment(account=os.getenv(
    'CDK_DEFAULT_ACCOUNT'), region='af-south-1')
euro_env = Environment(account=os.getenv(
    'CDK_DEFAULT_ACCOUNT'), region='eu-central-1')
alt_env = Environment(account=os.getenv(
    'CDK_DEFAULT_ACCOUNT'), region='us-east-1')

cross_account_a = app.node.try_get_context("cross_account_a")
cross_account_b = app.node.try_get_context("cross_account_b")

##############
# STACKS #
##############
enable_canary_stack = False
enable_lambda_stack = False
enable_eks_stack = False
enable_windows_stack = False
enable_batch_stack = False
enable_inspector_stack = False
enable_documentdb_stack = False
enable_autoscaling_stack = False
enable_machine_learning_stack = False
enable_acm_stack = False
enable_rds_stack = False
enable_efs_stack = False
enable_events_stack = False
enable_ssm_stack = False
enable_multi_target_alb_stack = True

# waf_stack = WafCloudFrontStack(app, "WafCloudFrontStack", removal_policy=RemovalPolicy.DESTROY, env=Environment(
#     account=os.getenv("CDK_DEFAULT_ACCOUNT"), region='us-east-1'
# ), )

net = NetworkingStack(
    app,
    "NetworkingStack",
    # waf=waf_stack.waf,
    removal_policy=RemovalPolicy.DESTROY,
    cross_region_references=True,
    env=default_env,
)

# analytics = AnalyticsStack(
#     app,
#     "AnalyticsStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# security = SecurityStack(
#     app,
#     "SecurityStack",
#     removal_policy=RemovalPolicy.DESTROY,
#     env=euro_env,
# )

if enable_events_stack:
    events = EventsStack(
        app,
        "EventsStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_lambda_stack:
    lambda_ = LambdaStack(
        app,
        "LambdaStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_ssm_stack:
    ssm = SsmStack(
        app,
        "SsmStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )    

if enable_efs_stack:
    efs = EfsStack(
        app,
        "EfsStack",
        vpc=net.vpc,
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_multi_target_alb_stack:
    MultiTargetAlbStack(
        app,
        "MultiTargetAlbStack",
        vpc=net.vpc,
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_rds_stack:
    rds = RdsStack(
        app,
        "RdsStack",
        vpc=net.vpc,
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_acm_stack:
    acm = CertificateManagerStack(
        app,
        "CertificateManagerStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_inspector_stack:
    inspector = InspectorStack(
        app,
        "InspectorStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_windows_stack:
    windows = WindowsStack(
        app,
        "WindowsStack",
        removal_policy=RemovalPolicy.DESTROY,
        key_name=key_name,
        vpc=net.vpc,
        whitelisted_peer=ec2.Peer.prefix_list(peers),
        env=default_env,
    )

# containers = ContainerStack(
#     app,
#     "ContainerStack",
#     # vpc=net.vpc,
#     image_name='farrout/reponderous:latest',
#     secret_arn=security.secret.secret_full_arn,
#     removal_policy=RemovalPolicy.DESTROY,
#     env=africa_env,
#     cross_region_references=True,
# )

if enable_eks_stack:
    eks = EksStack(
        app,
        "EksStack",
        # vpc=net.vpc,
        eks_version='1.24',
        removal_policy=RemovalPolicy.DESTROY,
        env=Environment(
            account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
        ),
    )


if enable_batch_stack:
    batch = BatchStack(
        app,
        "BatchStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=Environment(
            account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
        ),
    )

# ml = MachineLearningStack(
#     app,
#     "MachineLearningStack",
#     removal_policy=RemovalPolicy.DESTROY,
#     env=default_env,
# )

# canary_deployment = CanaryDeploymentStack(
#     app,
#     "CanaryDeploymentStack",
#     removal_policy=RemovalPolicy.DESTROY,
#     vpc=net.vpc,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# autoscaling = AutoscalingStack(
#     app,
#     "AutoscalingStack",
#     removal_policy=RemovalPolicy.DESTROY,
#     env=default_env,
# )

# docdb = DocumentDbStack(
#     app,
#     "DocumentDbStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

if enable_canary_stack:
    canary = CanaryStack(
        app,
        "CanaryStack",
        env=Environment(
            account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
        ),
    )

app.synth()
