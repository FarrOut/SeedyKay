from aws_cdk import (
    # Duration,
    NestedStack, aws_cloudwatch as cloudwatch,
    RemovalPolicy, CfnOutput, Tags, )
from constructs import Construct


class AlarmsNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        metric = cloudwatch.Metric(
            namespace="MyNamespace",
            metric_name="MyMetric",
            dimensions_map={
                "ProcessingStep": "Download"
            }
        )

        alarm = cloudwatch.Alarm(self, "Alarm",
                                 metric=metric,
                                 threshold=100,
                                 evaluation_periods=2
                                 )
        Tags.of(alarm).add('ThisTag', 'Was added at resource-level')

        cfn_alarm = alarm.node.default_child
        cfn_alarm.add_property_override("Tags.0.Value", "Raw override")

        CfnOutput(self, 'AlarmArn', value=alarm.alarm_arn, description='ARN of this alarm.')
        CfnOutput(self, 'AlarmName', value=alarm.alarm_name, description='Name of this alarm.')
        CfnOutput(self, 'AlarmMetricName', value=alarm.metric.metric_name,
                  description='The name of the metric this alarm was based on.')
