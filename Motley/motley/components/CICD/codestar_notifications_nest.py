from aws_cdk import (
    # Duration,
    Stack,
    aws_codepipeline as codepipeline,
    aws_s3 as s3,
    CfnOutput,
    aws_sns as sns,
    aws_codestarnotifications as notifications,
    NestedStack,
    aws_s3_deployment as s3deploy,
    RemovalPolicy,
)
from aws_cdk.aws_codepipeline import StageProps
from aws_cdk.aws_codepipeline_actions import (
    CloudFormationDeployStackSetAction,
    StackSetTemplate,
    StackSetDeploymentModel,
    StackInstances,
    S3SourceAction,
    S3Trigger,
)
from aws_cdk.aws_s3_deployment import BucketDeployment
from constructs import Construct


class CodeStarNotificationsNest(NestedStack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        pipeline: codepipeline.IPipeline,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        topic = sns.Topic(self, "MyTopic1")
        CfnOutput(self, "TopicArn", value=topic.topic_arn)

        rule = notifications.NotificationRule(
            self,
            "NotificationRule",
            source=pipeline,
            events=[
                "codepipeline-pipeline-action-execution-failed",
                "codepipeline-pipeline-pipeline-execution-started",
                "codepipeline-pipeline-pipeline-execution-succeeded",
            ],
            detail_type=notifications.DetailType.FULL,
            targets=[topic],
        )

        CfnOutput(self, "NotificationRuleArn", value=rule.notification_rule_arn)
