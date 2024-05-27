from aws_cdk import (
    # Duration,
    Stack, CfnOutput,
    aws_scheduler as scheduler, aws_lambda as lambda_, RemovalPolicy,
)
from aws_cdk.aws_iam import ManagedPolicy, Role, ServicePrincipal
from aws_cdk.aws_lambda import Runtime, Code
from aws_cdk.aws_scheduler import CfnSchedule
from constructs import Construct


class SchedulerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        managed_policy_arn = \
            ManagedPolicy.from_aws_managed_policy_name('AmazonEventBridgeSchedulerFullAccess')

        schedule_role = Role(self, "Role",
                             assumed_by=ServicePrincipal("scheduler.amazonaws.com"),
                             # custom description if desired
                             description="This is a custom role...",
                             managed_policies=[managed_policy_arn],
                             )
        schedule_role.apply_removal_policy(RemovalPolicy.DESTROY)

        fn = lambda_.Function(self, "lambda_function",
                              runtime=Runtime.NODEJS_18_X,
                              handler="index.handler",
                              code=Code.from_inline('exports.handler = handler.toString() //'))

        schedule_group = scheduler.CfnScheduleGroup(self, "MyScheduleGroup",
                                                    name="GroupOfSchedules", )

        CfnOutput(self, 'ScheduleGroupName',
                  description='The Name attribute of the schedule group.',
                  value=str(schedule_group.name)
                  )
        CfnOutput(self, 'ScheduleGroupArn',
                  description='The ARN of the schedule group.',
                  value=str(schedule_group.attr_arn)
                  )

        self.schedule = scheduler.CfnSchedule(self, "MyCfnSchedule",
                                              # name='theschedule',
                                              group_name=schedule_group.name,
                                              flexible_time_window=scheduler.CfnSchedule.FlexibleTimeWindowProperty(
                                                  mode="OFF",
                                              ),
                                              state='ENABLED',
                                              schedule_expression="rate(5 minutes)",
                                              schedule_expression_timezone="Europe/Berlin",
                                              target=CfnSchedule.TargetProperty(
                                                  arn=fn.function_arn,
                                                  role_arn=schedule_role.role_arn,
                                              ),
                                              )

        CfnOutput(self, 'ScheduleName',
                  description='The Name attribute of the schedule.',
                  value=str(self.schedule.ref)
                  )
        CfnOutput(self, 'ScheduleArn',
                  description='The ARN of the schedule.',
                  value=str(self.schedule.attr_arn)
                  )
