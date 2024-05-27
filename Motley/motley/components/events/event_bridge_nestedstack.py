from aws_cdk import CfnOutput, Duration, NestedStack, RemovalPolicy, Tags
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from aws_cdk import aws_iam as iam
from constructs import Construct


class EventBridgeNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        target = targets.AwsApi(
            action='sendCommandCommand',
            service="SSM",
            parameters={
                    "DocumentName": 'AWS-ApplyAnsiblePlaybooks',
                    "TimeoutSeconds": 60,
                    "Targets": [
                        {
                            "Key": 'tag:aws:autoscaling:groupName',
                            "Values": [
                                "Figure12",
                            ]
                        },
                    ]
            },
            # policy_statement=iam.PolicyStatement(
            #     actions=["ssm:SendCommand"],
            #     resources=["*"]
            # )
        )

        rule = events.Rule(
            self, "EatYourMeat",
            description='How can you have any pudding if you don\'t eat your meat?!',
            rule_name="EatYourMeat",
            schedule=events.Schedule.rate(Duration.minutes(1)),
            targets=[target],
        )
        rule.apply_removal_policy(removal_policy)

        CfnOutput(self, "RuleArn", value=rule.rule_arn,
                  description='events:us-east-2:123456789012:rule/example')
        CfnOutput(self, "RuleName", value=rule.rule_name,
                  description='The name of the rule.')
