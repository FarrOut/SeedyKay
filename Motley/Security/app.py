#!/usr/bin/env python3
import os

import aws_cdk as cdk

from security.secret_stack import SecretStack

app = cdk.App()
SecretStack(app, "SecretStack",
            env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
            )

app.synth()
