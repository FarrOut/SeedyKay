from aws_cdk import (
    # Duration,
    Stack,
    aws_events as events,
    aws_events_targets as targets,
    aws_logs as logs, RemovalPolicy
)
from aws_cdk.aws_events_targets import CloudWatchLogGroup
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct


class SenderStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, receiver_account: str, source: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bus = events.EventBus(self, "TheMagicSchoolbus",
                              event_bus_name="TheMagicSchoolbus"
                              )

        # Target another account's default eventbus
        remote_eventbus_target = targets.EventBus(
            events.EventBus.from_event_bus_arn(self, "External",
                                               "arn:aws:events:" +
                                               self.region + ":" + receiver_account +
                                               ":event-bus/default"))

        # LogGroup in which to log events
        log_group = logs.LogGroup(self, "EventBridgeLogGroup",
                                  removal_policy=RemovalPolicy.DESTROY,
                                  retention=RetentionDays.ONE_WEEK,
                                  )
        log_target = CloudWatchLogGroup(log_group)

        # Match events coming from 'source' and forward them to our LogGroup
        custom_rule = events.Rule(self, "CustomRule",
                                  event_bus=bus,
                                  event_pattern=events.EventPattern(
                                      source=[source]
                                  ),
                                  targets=[remote_eventbus_target, log_target],
                                  )

        backup_rule = events.Rule(self, "rule",
                                  # schedule=Schedule.rate(Duration.minutes(1)),
                                  targets=[remote_eventbus_target],
                                  event_pattern=events.EventPattern(
                                      source=["aws.backup"],
                                      detail_type=["Copy Job State Change"],
                                      detail={"state": ["COMPLETED"],
                                              "resourceType": ["RDS", "Aurora"],
                                              "destinationBackupVaultArn": [{
                                                  "prefix": "arn:aws:backup:us-east-1:00000000000000"
                                              }]},
                                  )
                                  )
