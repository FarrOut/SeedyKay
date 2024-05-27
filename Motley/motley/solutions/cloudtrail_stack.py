from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_ecs import ContainerImage
from constructs import Construct
from motley.components.analytics.cloudtrail_nestedstack import CloudTrailNestedStack
from motley.components.security.ssm_document_nestedstack import SsmDocumentNestedStack

from motley.components.events.alarms_nestedstack import AlarmsNestedStack


class CloudTrailStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        trail_stack = CloudTrailNestedStack(self, 'CloudTrailNestedStack',
                                            removal_policy=removal_policy,
                                            )
