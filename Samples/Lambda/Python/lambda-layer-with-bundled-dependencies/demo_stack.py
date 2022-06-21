from aws_cdk import (
    core as cdk,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_lambda_python import PythonLayerVersion, PythonFunction
from aws_cdk.core import RemovalPolicy


class DemoStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        asset_dir = './assets/'

        fn = PythonFunction(self, "MyPythonFunction",
                            entry=asset_dir,  # required
                            index="script.py",  # optional, defaults to 'index.py'
                            handler="handler",  # optional, defaults to 'handler'
                            runtime=Runtime.PYTHON_3_9,
                            layers=[
                                PythonLayerVersion(self, "MyFirstLayer",
                                                   entry=asset_dir,
                                                   compatible_runtimes=[Runtime.PYTHON_3_9, Runtime.PYTHON_3_8],
                                                   description='Extend base function to import and bundle a package dependency',
                                                   removal_policy=RemovalPolicy.DESTROY,
                                                   )],
                            )
