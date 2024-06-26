from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, Tags, aws_ec2 as ec2, aws_sns as sns, Duration,
)
from constructs import Construct
from motley.components.analytics.cloudwatch_dashboard_nestedstack import CloudWatchDashboardNestedStack
from motley.components.analytics.cloudwatch_lambda_alarms_nestedstack import CloudWatchLambdaAlarmsNestedStack
from motley.components.networking.vpc_stack import VpcNestedStack
from motley.computing.lambda_nestedstack import LambdaNestedStack
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets


class CloudWatchStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 vpc: ec2.IVpc = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function = LambdaNestedStack(self, "LambdaNestedStack",
                                     vpc=vpc, removal_policy=removal_policy).function

        rule = events.Rule(
            self, "EatYourMeat",
            description='How can you have any pudding if you don\'t eat your meat?!',
            rule_name="EatYourMeat",
            schedule=events.Schedule.rate(Duration.minutes(1)),
            targets=[targets.LambdaFunction(function,
                                            # Optional: set the maxEventAge retry policy
                                            max_event_age=Duration.hours(2),
                                            retry_attempts=2
                                            )],
        )
        rule.apply_removal_policy(removal_policy)

        cfn_rule = rule.node.default_child
        # cfn_rule.add_property_override("Tags.0.Value", "Resource-level tag")
        Tags.of(rule).add("Note", "Resource-level-tag L2")
        Tags.of(cfn_rule).add("Note", "Resource-level-tag L1")
        # aws cloudformation describe-type --type-name AWS::CloudWatch::Alarm --type RESOURCE

        topic = sns.Topic(self, "Topic",
                          display_name="Lambda alarms"
                          )

        CloudWatchLambdaAlarmsNestedStack(
            self, "CloudWatchLambdaAlarmsNestedStack", function=function, topic=topic, removal_policy=removal_policy)

        CloudWatchDashboardNestedStack(
            self, "CloudWatchDashboardNestedStack",  removal_policy=removal_policy)
