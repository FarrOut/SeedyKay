from aws_cdk import (
    # Duration,
    NestedStack, aws_cloudwatch as cloudwatch, aws_iot as iot, aws_iam as iam,
    RemovalPolicy, CfnOutput, Tags, )
from constructs import Construct


class IoTloggingNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 account_id: int,
                 role: iam.IRole,
                 default_log_level: str = "INFO",
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        logging = iot.CfnLogging(self, "MyCfnLogging",
                                 account_id=account_id,
                                 default_log_level=default_log_level,
                                 role_arn=role.role_arn,
                                 )
        logging.apply_removal_policy(removal_policy)
        
        CfnOutput(self, "LoggingAccountId", value=logging.account_id, description="The account ID.")
        CfnOutput(self, "DefaultLoggingLevel", value=logging.default_log_level, description="The default log level.")
        CfnOutput(self, "LoggingRoleArn", value=logging.role_arn, description="The role ARN used for the log.")
        