#!/usr/bin/env python3
import os

from aws_cdk import (

    aws_ec2 as ec2, App, Environment
)

from motley.computing.windows_instance_stack import WindowsInstanceStack
from motley.networking.networking_stack import NetworkingStack
from motley.security.kms_stack import KmsStack
from motley.security.secret_stack import SecretStack
from motley.security.ssm_stack import SsmStack
from motley.storage.backup_stack import BackupStack
from motley.storage.ecr_stack import EcrStack

app = App()
peers = app.node.try_get_context("peers")
app_name = 'motley'

net = NetworkingStack(app, "{}-NetworkingStack".format(app_name),
                      existing_vpc_id=app.node.try_get_context("existing_vpc_id"),
                      env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                      region=os.getenv('CDK_DEFAULT_REGION')),
                      )

secrets = SecretStack(app, "SecretStack",
                      vpc=net.vpc,
                      env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                      region=os.getenv('CDK_DEFAULT_REGION')),
                      )

ssm = SsmStack(app, "SsmStack",
               env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                               region=os.getenv('CDK_DEFAULT_REGION')),
               )

kms = KmsStack(app, "KmsStack",
               env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                               region=os.getenv('CDK_DEFAULT_REGION')),
               )

backup = BackupStack(app, "BackupStack",
                     env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                     region=os.getenv('CDK_DEFAULT_REGION')),
                     )

ecr = EcrStack(app, "EcrStack",
               env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                               region=os.getenv('CDK_DEFAULT_REGION')),
               )

windows_instances = WindowsInstanceStack(app, "WindowsInstanceStack",
                                         key_name=app.node.try_get_context("key_name"),
                                         whitelisted_peer=ec2.Peer.prefix_list(peers),
                                         vpc=net.vpc,
                                         env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                                         region=os.getenv('CDK_DEFAULT_REGION')),
                                         )

app.synth()
