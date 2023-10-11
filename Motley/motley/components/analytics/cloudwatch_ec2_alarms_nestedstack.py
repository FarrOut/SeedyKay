from aws_cdk import (
    # Duration,
    aws_synthetics_alpha as synthetics, aws_lambda as lambda_, aws_cloudwatch as cloudwatch,aws_ec2 as ec2,
    NestedStack, RemovalPolicy, Duration, CfnOutput, )
from aws_cdk.aws_synthetics_alpha import Code, RuntimeFamily
from constructs import Construct


class CloudWatchEc2AlarmsNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 instance: ec2.Instance,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # cpu_metric = cloudwatch.Metric(
        #     namespace="AWS/EC2",
        #     metric_name="CpuUsage",
        #     dimensionsMap=dict(MyDimension="MyDimensionValue")
        # )

        # cpu_alarm = cloudwatch.Alarm(self, "Alarm",
        #                              metric=cpu_metric,
        #                              threshold=100,
        #                              evaluation_periods=2
        #                              )
        # cpu_alarm.apply_removal_policy(removal_policy)

        # CfnOutput(self, 'CpuUsageAlarmArn', value=cpu_alarm.alarm_arn,
        #           description='Arn of CPU usage alarm.')
        # CfnOutput(self, 'CpuUsageAlarmName', value=cpu_alarm.alarm_name,
        #           description='Name of CPU usage alarm.')