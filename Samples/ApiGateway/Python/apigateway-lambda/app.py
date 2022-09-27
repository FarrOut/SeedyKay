#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lab.infra_stack import InfraStack
from lab.lab_stack import LabStack
from lab.solutions_stack import SolutionsStack

app = cdk.App()

infra = InfraStack(app, "InfraStack",
                   env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                       region=os.getenv('CDK_DEFAULT_REGION')),
                   )

LabStack(app, "LabStack",
         rest_api_id=infra.rest_api_id,
         request_model=infra.request_model,
         rest_api_root_resource_id=infra.rest_api_root_resource_id,
         env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
         )

SolutionsStack(app, "SolutionsStack",
               env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                   region=os.getenv('CDK_DEFAULT_REGION')),
               )

app.synth()
