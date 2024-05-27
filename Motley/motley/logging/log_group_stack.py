from aws_cdk import (
    # Duration,
    Stack, CfnOutput, RemovalPolicy, )
from aws_cdk.aws_logs import LogGroup, RetentionDays
from constructs import Construct


class LogGroupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.log_group = LogGroup(self, "LogGroup",
                                  retention=RetentionDays.ONE_WEEK,
                                  removal_policy=RemovalPolicy.DESTROY
                                  )

        CfnOutput(self, 'LogGroupArn',
                  description='The ARN of this log group.',
                  value=self.log_group.log_group_arn
                  )
        CfnOutput(self, 'LogGroupName',
                  description='The name of this log group.',
                  value=self.log_group.log_group_name
                  )
