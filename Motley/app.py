#!/usr/bin/env python3
import os

import boto3
from aws_cdk import RemovalPolicy, App, Environment

from motley.CICD.canary_deployment_stack import CanaryDeploymentStack
from motley.networking.networking_stack import NetworkingStack
from motley.solutions.eks_stack import EksStack

secretsmanager_ = boto3.client("secretsmanager")

app = App()
peers = app.node.try_get_context("peers")
app_name = "motley"

cross_account_a = app.node.try_get_context("cross_account_a")
cross_account_b = app.node.try_get_context("cross_account_b")

net = NetworkingStack(
    app,
    "NetworkingStack",
    existing_vpc_id=app.node.try_get_context("existing_vpc_id"),
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

# secrets = SecretStack(
#     app,
#     "SecretStack",
#     vpc=net.vpc,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# security_groups = SecurityGroupsStack(
#     app,
#     "SecurityGroupsStack",
#     vpc=net.vpc,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# ssm = SsmStack(
#     app,
#     "SsmStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

eks = EksStack(
    app,
    "Eks",
    vpc=net.vpc,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

# imported_eks = ImportedEksStack(
#     app,
#     "ImportedEksStack",
#     vpc=net.vpc,
#     cluster=eks.cluster,
#     kubectl_provider=eks.provider,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# ecs = EcsStack(
#     app,
#     "EcsStack",
#     vpc=net.vpc,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# kms = KmsStack(
#     app,
#     "KmsStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# backup = BackupStack(
#     app,
#     "BackupStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# # acm = AcmStack(
# #     app,
# #     "AcmStack",
# #     env=Environment(
# #         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
# #     ),
# # )

# rds = RdsStack(
#     app,
#     "RdsStack",
#     vpc=net.vpc,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# rds_serverless = RdsServerlessStack(
#     app,
#     "RdsServerlessStack",
#     vpc=net.vpc,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# s3 = S3Stack(
#     app,
#     "S3Stack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# kinesis = KinesisStack(
#     app,
#     "KinesisStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# ecr = EcrStack(
#     app,
#     "EcrStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# opensearch = OpenSearchStack(
#     app,
#     "OpenSearchStack",
#     version=EngineVersion.OPENSEARCH_1_3,
#     vpc=net.vpc,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# scheduler = SchedulerStack(
#     app,
#     "SchedulerStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# dynamodb = DynamoDBStack(
#     app,
#     "DynamoDbStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# r53 = Route53Stack(
#     app,
#     "Route53Stack",
#     vpc=net.vpc,
#     zone_name="dangerzone.kennyrogers.com",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# logs = LogGroupStack(
#     app,
#     "LogGroupStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# waf = WafStack(
#     app,
#     "WafStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# elasticache = ElastiCacheStack(
#     app,
#     "ElastiCacheStack",
#     vpc=net.vpc,
#     log_group=logs.log_group,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# ad = DirectoryStack(
#     app,
#     "DirectoryStack",
#     vpc=net.vpc,
#     domain_name="dangerzone.kennyrogers.com",
#     password="WagW00rd!",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# fsx = FSxStack(
#     app,
#     "FSxStack",
#     vpc=net.vpc,
#     # domain_name=r53.zone.zone_name,
#     active_directory=ad.ad,
#     # domain_name='corp.example.com',
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# windows_instances = WindowsInstanceStack(
#     app,
#     "WindowsInstanceStack",
#     key_name=app.node.try_get_context("key_name"),
#     whitelisted_peer=ec2.Peer.prefix_list(peers),
#     vpc=net.vpc,
#     bucket=s3.bucket,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# cross_account_pipeline = CrossAccountCodePipelineStack(
#     app,
#     "CrossAccountCodePipelineStack",
#     remote_account=cross_account_a,
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

# asg = AutoScalingStack(
#     app,
#     "AutoScalingStack",
#     removal_policy=RemovalPolicy.DESTROY,
#     vpc=net.vpc,
#     key_name=app.node.try_get_context("key_name"),
#     whitelisted_peer=ec2.Peer.prefix_list(peers),
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

canary_deployment = CanaryDeploymentStack(
    app,
    "CanaryDeploymentStack",
    removal_policy=RemovalPolicy.DESTROY,
    vpc=net.vpc,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

app.synth()
