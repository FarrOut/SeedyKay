from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_ecs import ContainerImage
from constructs import Construct
from motley.components.events.event_bridge_nestedstack import EventBridgeNestedStack

from motley.components.events.alarms_nestedstack import AlarmsNestedStack


class EventsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # self.alarms = AlarmsNestedStack(self, "AlarmsNestedStack", removal_policy=removal_policy)

        self.events = EventBridgeNestedStack(self, "EventBridgeNestedStack", removal_policy=removal_policy,                                             
                                             )
