from aws_cdk import (
    # Duration,
    Stack,
    aws_events as events,
    aws_logs as logs, RemovalPolicy, CfnOutput
)
from aws_cdk.aws_events import EventBus, CfnEventBusPolicy
from aws_cdk.aws_events_targets import CloudWatchLogGroup
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct


class ReceiverStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, source: str, sender_account: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import default bus
        default_bus = EventBus.from_event_bus_name(self, 'DefaultEventBus', 'default')
        CfnOutput(self, 'DefaultEventBusArn',
                  value=default_bus.event_bus_arn,
                  description='Arn of imported default EventBus')

        # Permissions for event buses
        # https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus-perms.html
        CfnEventBusPolicy(self, 'DefaultEventBusCrossAccountPolicy',
                          statement_id='AllowEventsFromAnotherAccount',
                          action='events:PutEvents',
                          event_bus_name=default_bus.event_bus_name,
                          principal=sender_account,
                          )

        # LogGroup in which to log events
        log_group = logs.LogGroup(self, "EventBridgeLogGroup",
                                  removal_policy=RemovalPolicy.DESTROY,
                                  retention=RetentionDays.ONE_WEEK,
                                  )
        log_target = CloudWatchLogGroup(log_group)

        # Match events coming from 'source' and forward them to our LogGroup
        rule = events.Rule(self, "CustomRule",
                           event_pattern=events.EventPattern(
                               source=[source]
                           ),
                           targets=[log_target],
                           )
