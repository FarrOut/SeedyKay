from aws_cdk import (
    # Duration,
    NestedStack, aws_efs as efs, PhysicalName, aws_kms as kms, aws_lambda_python_alpha as python,
    aws_ec2 as ec2, aws_lambda as lambda_, RemovalPolicy, CfnOutput, )
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy
from aws_cdk.aws_lambda import Runtime, Code
from constructs import Construct

from motley.components.storage.filesystems.efs_nestedstack import EfsNestedStack
from motley.computing.lambda_nestedstack import LambdaNestedStack


class LayeredLambdaNest(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 # file_system: lambda_.FileSystem = None,
                 vpc: ec2.IVpc = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fn = python.PythonFunction(self, "MyFunction",
                                   entry="./motley/computing/layers/consumers",  # required
                                   runtime=Runtime.PYTHON_3_12,  # required
                                   index="consumer.py",  # optional, defaults to 'index.py'
                                   handler="handler"
                                   )

        layer = python.PythonLayerVersion(self, "MyLayer",
                                          entry="./motley/computing/layers/splunk_hec_logger",
                                          removal_policy=removal_policy,
                                          compatible_runtimes=[
                                              Runtime.PYTHON_3_12],
                                          )
        fn.add_layers(layer)
