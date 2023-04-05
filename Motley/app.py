#!/usr/bin/env python3
import os

from aws_cdk import (

    aws_ec2 as ec2, App, Environment
)

from motley.computing.windows_instance_stack import WindowsInstanceStack
from motley.networking.networking_stack import NetworkingStack

app = App()
peers = app.node.try_get_context("peers")
net = NetworkingStack(app, "NetworkingStack",
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
