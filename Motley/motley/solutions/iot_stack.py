from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2, aws_iot as iot,
    RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_ecs import ContainerImage
from constructs import Construct

from motley.components.iot.iot_nestedstack import IoTNestedStack


class IoTStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        IoTNestedStack(self, 'IoTNestedStack',
                       removal_policy=removal_policy,
                       )
