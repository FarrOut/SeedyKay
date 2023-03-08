#!/usr/bin/env python3
import os

import aws_cdk as cdk

from computing.autoscaling_stack import AutoScalingStack
from computing.networking_stack import NetworkingStack

app = cdk.App()

net = NetworkingStack(app, "NetworkingStack",
                      env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                          region=os.getenv('CDK_DEFAULT_REGION')),
                      )

AutoScalingStack(app, "AutoScalingStack",
                 vpc=net.vpc,
                 env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
                 )

app.synth()
