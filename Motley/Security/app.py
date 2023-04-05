#!/usr/bin/env python3
import os

import aws_cdk as cdk

from security.networking_stack import NetworkingStack
from security.secret_stack import SecretStack

app = cdk.App()

net = NetworkingStack(app, "NetworkingStack",
                      env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                          region=os.getenv('CDK_DEFAULT_REGION')),
                      )

SecretStack(app, "SecretStack",
            vpc=net.vpc,
            env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
            )

app.synth()
