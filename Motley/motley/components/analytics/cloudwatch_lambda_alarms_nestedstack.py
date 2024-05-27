from aws_cdk import (
    # Duration,
    aws_synthetics_alpha as synthetics, aws_lambda as lambda_, aws_cloudwatch as cloudwatch, aws_ec2 as ec2, aws_sns as sns, aws_cloudwatch_actions as cw_actions,
    NestedStack, RemovalPolicy, Duration, CfnOutput, )
from aws_cdk.aws_synthetics_alpha import Code, RuntimeFamily
from constructs import Construct


class CloudWatchLambdaAlarmsNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 function: lambda_.IFunction,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 topic: sns.ITopic = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dimensions = {"FunctionName": function.function_name}

        # #######
        # ERRORS
        # #######

        errors_alarm = cloudwatch.Alarm(self, "ErrorAlarm",
                                        comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                        threshold=1,
                                        evaluation_periods=3,
                                        metric=function.metric_errors(
                                            dimensions_map=dimensions)
                                        )
        errors_alarm.apply_removal_policy(removal_policy)

        if topic is not None:
            errors_alarm.add_alarm_action(cw_actions.SnsAction(topic))

        CfnOutput(self, 'ErrorsAlarmArn', value=errors_alarm.alarm_arn,
                  description='Arn of invocation errors alarm.')
        CfnOutput(self, 'ErrorsAlarmName', value=errors_alarm.alarm_name,
                  description='Name of invocation errors alarm.')

        # #######
        # INVOCATIONS
        # #######

        invocations_alarm = cloudwatch.Alarm(self, "InvocationAlarm",
                                             comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
                                             threshold=10,
                                             evaluation_periods=2,
                                             metric=function.metric_invocations(
                                                 dimensions_map=dimensions)
                                             )
        invocations_alarm.apply_removal_policy(removal_policy)

        if topic is not None:
            invocations_alarm.add_alarm_action(cw_actions.SnsAction(topic))

        CfnOutput(self, 'InvocationsAlarmArn', value=invocations_alarm.alarm_arn,
                  description='Arn of invocations alarm.')
        CfnOutput(self, 'InvocationsAlarmName', value=invocations_alarm.alarm_name,
                  description='Name of invocations alarm.')
