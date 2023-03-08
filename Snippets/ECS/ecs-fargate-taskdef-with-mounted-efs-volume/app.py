#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lab.lab_stack import LabStack
from lab.infra_stack import InfraStack

app = cdk.App()
infra_stack = InfraStack(app, "InfraStack",
                         env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                             region=os.getenv('CDK_DEFAULT_REGION')),
                         )

LabStack(app, "LabStack",
         file_system=infra_stack.file_system,
         vpc=infra_stack.vpc,
         security_group_id='sg-xxxxxxxxxx',


         env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

         )

app.synth()
