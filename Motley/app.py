#!/usr/bin/env python3
import os

import boto3
from aws_cdk import aws_ec2 as ec2, App, Environment

from motley.CICD.cross_account.cross_account_codepipeline_stack import (
    CrossAccountCodePipelineStack,
)
from motley.analytics.kinesis_stack import KinesisStack
from motley.computing.windows_instance_stack import WindowsInstanceStack
from motley.containerization.ecr_stack import EcrStack
from motley.containerization.ecs_stack import EcsStack
from motley.events.scheduler_group_stack import SchedulerStack
from motley.logging.log_group_stack import LogGroupStack
from motley.networking.networking_stack import NetworkingStack
from motley.networking.route53_stack import Route53Stack
from motley.orchestration.eks_stack import EksStack
from motley.orchestration.imported_eks_stack import ImportedEksStack
from motley.security.acm_stack import AcmStack
from motley.security.kms_stack import KmsStack
from motley.security.secret_stack import SecretStack
from motley.security.security_groups_stack import SecurityGroupsStack
from motley.security.ssm_stack import SsmStack
from motley.security.waf_stack import WafStack
from motley.storage.backup.backup_stack import BackupStack
from motley.storage.block.s3_stack import S3Stack
from motley.storage.databases.elasticache_stack import ElastiCacheStack
from motley.storage.databases.rds_serverless_stack import RdsServerlessStack
from motley.storage.databases.rds_stack import RdsStack
from motley.storage.filesystems.directory_stack import DirectoryStack
from motley.storage.filesystems.fsx_stack import FSxStack

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

secrets = SecretStack(
    app,
    "SecretStack",
    vpc=net.vpc,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

security_groups = SecurityGroupsStack(
    app,
    "SecurityGroupsStack",
    vpc=net.vpc,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

ssm = SsmStack(
    app,
    "SsmStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

eks = EksStack(
    app,
    "EksStack",
    vpc=net.vpc,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

imported_eks = ImportedEksStack(
    app,
    "ImportedEksStack",
    vpc=net.vpc,
    cluster=eks.cluster,
    kubectl_provider=eks.provider,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

ecs = EcsStack(
    app,
    "EcsStack",
    vpc=net.vpc,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

kms = KmsStack(
    app,
    "KmsStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

backup = BackupStack(
    app,
    "BackupStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

# acm = AcmStack(
#     app,
#     "AcmStack",
#     env=Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
#     ),
# )

rds = RdsStack(
    app,
    "RdsStack",
    vpc=net.vpc,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

rds_serverless = RdsServerlessStack(
    app,
    "RdsServerlessStack",
    vpc=net.vpc,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

s3 = S3Stack(
    app,
    "S3Stack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

kinesis = KinesisStack(
    app,
    "KinesisStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

ecr = EcrStack(
    app,
    "EcrStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

scheduler = SchedulerStack(
    app,
    "SchedulerStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

r53 = Route53Stack(
    app,
    "Route53Stack",
    vpc=net.vpc,
    zone_name="dangerzone.kennyrogers.com",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

logs = LogGroupStack(
    app,
    "LogGroupStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

waf = WafStack(
    app,
    "WafStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

elasticache = ElastiCacheStack(
    app,
    "ElastiCacheStack",
    vpc=net.vpc,
    log_group=logs.log_group,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

ad = DirectoryStack(
    app,
    "DirectoryStack",
    vpc=net.vpc,
    domain_name="dangerzone.kennyrogers.com",
    password="WagW00rd!",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

fsx = FSxStack(
    app,
    "FSxStack",
    vpc=net.vpc,
    # domain_name=r53.zone.zone_name,
    active_directory=ad.ad,
    # domain_name='corp.example.com',
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

windows_instances = WindowsInstanceStack(
    app,
    "WindowsInstanceStack",
    key_name=app.node.try_get_context("key_name"),
    whitelisted_peer=ec2.Peer.prefix_list(peers),
    vpc=net.vpc,
    bucket=s3.bucket,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

cross_account_pipeline = CrossAccountCodePipelineStack(
    app,
    "CrossAccountCodePipelineStack",
    remote_account=cross_account_a,
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

app.synth()
