#!/usr/bin/env python3
import os

from aws_cdk import (
    # Duration,
    Tags,
    aws_ec2 as ec2,
    aws_iam as iam,
    RemovalPolicy,
    App,
    Environment,
)

from motley.solutions.appconfig_stack import AppConfigStack
from motley.solutions.cloudtrail_stack import CloudTrailStack
from motley.solutions.codebuild_stack import CodeBuildStack
from motley.solutions.codestar_stack import CodeStarStack
from motley.solutions.config_stack import ConfigStack
from motley.solutions.custom_resource_stack import CustomResourceStack
from motley.solutions.ec2_stack import Ec2Stack
from motley.solutions.guard_duty_stack import GuardDutyStack
from motley.solutions.kms_stack import KmsStack
from motley.solutions.lakeformation_stack import LakeFormationStack
from motley.solutions.r53_stack import Route53Stack
from motley.solutions.service_catalog_stack import ServiceCatalogStack
from motley.solutions.machine_learning_stack import MachineLearningStack
from motley.solutions.flat_cloudmap_stack import CloudMapStack
from motley.solutions.ecr_stack import EcrStack
from motley.solutions.iot_stack import IoTStack
from motley.solutions.security_stack import SecurityStack
from motley.solutions.alb_fargate_service_stack import AlbFargateServiceStack
from motley.solutions.stacksets_stack import StackSetsStack
from motley.solutions.s3_stack import S3Stack
from motley.solutions.cloudwatch_stack import CloudWatchStack
from motley.solutions.apigateway_stack import ApiGatewayStack

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
from motley.solutions.vpc_endpoint_stack import VpcEndpointStack
from motley.solutions.windows_stack import WindowsStack
from motley.components.analytics.lakeformation_nestedstack import LakeFormation

app = App(
    # Include construct creation stack trace in the aws:cdk:trace metadata key of all constructs. Default: true stack traces are included unless aws:cdk:disable-stack-trace is set in the context.
    stack_traces=False,
    # Include construct tree metadata as part of the Cloud Assembly. Default: true
    tree_metadata=True,
)
peers = app.node.try_get_context("peers")
key_name = app.node.try_get_context("key_name")
debug_mode = bool(app.node.try_get_context("debug_mode"))


if debug_mode:
    print("Debug mode is enabled")

app_name = "motley"

default_env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
)
africa_env = Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region="af-south-1")
euro_env = Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region="eu-central-1")
alt_env = Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region="us-east-1")

cross_account_a = app.node.try_get_context("cross_account_a")
cross_account_b = app.node.try_get_context("cross_account_b")

##############
# STACKS #
##############
enable_acm_stack = False
enable_apigateway_stack = False
enable_appconfig_stack = True
enable_autoscaling_stack = False
enable_batch_stack = False
enable_canary_stack = False
enable_cloudmap_stack = False
enable_cloudtrail_stack = False
enable_cloudwatch_stack = False
enable_codebuild_stack = False
enable_codestar_stack = False
enable_config_stack = False
enable_custom_resource_stack = False
enable_documentdb_stack = False
enable_ec2_stack = False
enable_ecr_stack = False
enable_ecs_pattern_stack = False
enable_efs_stack = False
enable_eks_stack = False
enable_events_stack = False
enable_guard_duty_stack = False
enable_inspector_stack = False
enable_iot_stack = False
enable_kms_stack = False
enable_lake_formation_stack = False
enable_lambda_stack = False
enable_machine_learning_stack = False
enable_multi_target_alb_stack = False
enable_rds_stack = False
enable_r53_stack = False
enable_s3_stack = False
enable_security_stack = False
enable_service_catalog_stack = False
enable_ssm_stack = False
enable_stacksets_stack = False
enable_vpc_endpoint_stack = False
enable_windows_stack = False

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

if enable_vpc_endpoint_stack:
    VpcEndpointStack(
        app,
        "VpcEndpointStack",
        vpc=net.vpc,
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_appconfig_stack:
    AppConfigStack(
        app,
        "AppConfigStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_r53_stack:
    Route53Stack(
        app,
        "R53Stack",
        vpc=net.vpc,
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_kms_stack:
    KmsStack(
        app,
        "KmsStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_codebuild_stack:
    CodeBuildStack(
        app,
        "CodeBuildStack",
        removal_policy=RemovalPolicy.DESTROY,
        vpc=net.vpc,
        env=default_env,
    )

if enable_codestar_stack:
    CodeStarStack(
        app,
        "CodeStarStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_custom_resource_stack:
    endpoint = VpcEndpointStack(
        app,
        "VpcEndpointStack",
        vpc=net.vpc,
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    ).endpoint
    CustomResourceStack(
        app,
        "CustomResourceStack",
        vpc_endpoint=endpoint,
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )


if enable_cloudtrail_stack:
    CloudTrailStack(
        app,
        "CloudTrailStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_config_stack:
    ConfigStack(
        app,
        "ConfigStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_guard_duty_stack:
    GuardDutyStack(
        app,
        "GuardDutyStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_ec2_stack:
    Ec2Stack(
        app,
        "Ec2Stack",
        vpc=net.vpc,
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

# analytics = AnalyticsStack(
#     app,
#     "AnalyticsStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

if enable_ecr_stack:
    EcrStack(
        app,
        "EcrStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_lake_formation_stack:
    lake = LakeFormationStack(
        app,
        "LakeFormationStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )
    LakeFormation(
        app,
        "LakeFormationStack1",
        identifier="1",
        env=default_env,
        database=lake.database,
        role=lake.role,
        removal_policy=RemovalPolicy.DESTROY,
    )

    LakeFormation(
        app,
        "LakeFormationStack2",
        identifier="2",
        env=default_env,
        database=lake.database,
        role=lake.role,
        removal_policy=RemovalPolicy.DESTROY,
    )
    LakeFormation(
        app,
        "LakeFormationStack3",
        identifier="3",
        database=lake.database,
        role=lake.role,
        env=default_env,
        removal_policy=RemovalPolicy.DESTROY,
    )

if enable_service_catalog_stack:
    ServiceCatalogStack(
        app,
        "ServiceCatalogStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_cloudmap_stack:
    CloudMapStack(
        app,
        "CloudMapStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_security_stack:
    security = SecurityStack(
        app,
        "SecurityStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_iot_stack:
    IoTStack(
        app,
        "IoTStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_stacksets_stack:
    StackSetsStack(
        app,
        "StackSetsStack",
        deployment_ou_id=app.node.try_get_context("deployment_ou_id"),
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_apigateway_stack:
    api_gw = ApiGatewayStack(
        app,
        "ApiGatewayStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_ecs_pattern_stack:
    AlbFargateServiceStack(
        app,
        "AlbFargateServiceStack",
        # vpc=net.vpc,
        vpc_id="vpc-08ec4c9b2b7d0fcb0",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_s3_stack:
    s3 = S3Stack(
        app,
        "S3Stack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_cloudwatch_stack:
    cw = CloudWatchStack(
        app,
        "CloudWatchStack",
        vpc=net.vpc,
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )
    Tags.of(cw).add("Note", "Stack-level-tag")

if enable_events_stack:
    events = EventsStack(
        app,
        "EventsStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
    )

if enable_lambda_stack:
    LambdaStack(
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
        eks_version="1.24",
        removal_policy=RemovalPolicy.DESTROY,
        env=Environment(
            account=os.getenv("CDK_DEFAULT_ACCOUNT"),
            region=os.getenv("CDK_DEFAULT_REGION"),
        ),
    )


if enable_batch_stack:
    batch = BatchStack(
        app,
        "BatchStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=Environment(
            account=os.getenv("CDK_DEFAULT_ACCOUNT"),
            region=os.getenv("CDK_DEFAULT_REGION"),
        ),
    )

if enable_machine_learning_stack:
    ml = MachineLearningStack(
        app,
        "MachineLearningStack",
        removal_policy=RemovalPolicy.DESTROY,
        env=default_env,
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
            account=os.getenv("CDK_DEFAULT_ACCOUNT"),
            region=os.getenv("CDK_DEFAULT_REGION"),
        ),
    )

app.synth(
    force=debug_mode,  # Force a re-synth, even if the stage has already been synthesized. This is used by tests to allow for incremental verification of the output. Do not use in production. Default: false
)
