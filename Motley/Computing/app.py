#!/usr/bin/env python3
import os

from aws_cdk import (

    aws_ec2 as ec2,
    Environment, App
)

from computing.autoscaling_stack import AutoScalingStack
from computing.networking_stack import NetworkingStack

app = App()

peers = app.node.try_get_context("peers")
net = NetworkingStack(app, "NetworkingStack",
                      env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                      region=os.getenv('CDK_DEFAULT_REGION')),
                      )

AutoScalingStack(app, "AutoScalingStack",
                 vpc=net.vpc,
                 key_name=app.node.try_get_context("key_name"),
                 whitelisted_peer=ec2.Peer.prefix_list(peers),
                 env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
                 )

app.synth()
