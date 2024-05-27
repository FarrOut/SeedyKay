from aws_cdk import (
    # Duration,
    aws_ec2 as ec2,
    Stack, RemovalPolicy,
)
from constructs import Construct
from motley.components.security.inspector_classic_nestedstack import InspectorClassicNestedStack
from motley.components.security.inspector_v2_nestedstack import InspectorV2NestedStack
from motley.components.storage.block.bucket_deployment_nestedstack import BucketDeploymentNestedStack
from motley.components.networking.vpc_stack import VpcNestedStack
from motley.computing.windows_instance_stack import WindowsInstanceStack

from motley.components.analytics.canary_nestedstack import CanaryNestedStack
from motley.components.analytics.forecast_stack import ForecastStack


class InspectorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 vpc: ec2.IVpc = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dep = BucketDeploymentNestedStack(
            self, 'BucketDeploymentNestedStack',
            removal_policy=removal_policy,
            auto_delete_objects=True,
            prune=True,
        )

        # InspectorClassicNestedStack(self, 'InspectorClassicNestedStack',
        #                      removal_policy=removal_policy,
        #                      )
        # InspectorV2NestedStack(self, 'InspectorV2NestedStack',
        #                      removal_policy=removal_policy,
        #                      )
