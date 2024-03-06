from aws_cdk import (
    # Duration,
    NestedStack, aws_cloudwatch as cloudwatch, aws_iot as iot, aws_iam as iam, aws_lambda as lambda__,
    RemovalPolicy, CfnOutput, Tags, )
from constructs import Construct


class IoTRulesNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 function: lambda__.IFunction,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        topic_rule = iot.CfnTopicRule(self, "MyCfnTopicRule",
                                      rule_name='test_rule',
                                      topic_rule_payload=iot.CfnTopicRule.TopicRulePayloadProperty(
                                          actions=[iot.CfnTopicRule.ActionProperty(
                                              lambda_=iot.CfnTopicRule.LambdaActionProperty(
                                                  function_arn=function.function_arn
                                              )
                                          )],
                                          sql="SELECT * FROM '/dev/notification/dca'"
                                      ),
                                      )

        topic_rule.apply_removal_policy(removal_policy)

        # CfnOutput(self, "LoggingAccountId", value=logging.account_id, description="The account ID.")
        # CfnOutput(self, "DefaultLoggingLevel", value=logging.default_log_level, description="The default log level.")
        # CfnOutput(self, "LoggingRoleArn", value=logging.role_arn, description="The role ARN used for the log.")
