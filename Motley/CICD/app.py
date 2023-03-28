#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cicd.codepipeline_stack import CodePipelineStack

app = cdk.App()
CodePipelineStack(app, "CodePipelineStack",
                  env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
                  )

app.synth()
