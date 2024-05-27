from aws_cdk import (
    # Duration,
    NestedStack, RemovalPolicy, CfnOutput, aws_config as config, aws_iam as iam, aws_events_targets as targets, aws_sns as sns, aws_events as events,
)

from constructs import Construct


class ConfigRulesNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 service_role: iam.IRole = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cloudformation_drift_check = config.CloudFormationStackDriftDetectionCheck(self, 'CloudformationDriftCheck',
                                                                                   own_stack_only=False,  # Default: False
                                                                                   role=service_role,
                                                                                   config_rule_name='CloudformationDriftDetectionRule',
                                                                                   description='Checks whether your CloudFormation stacks’ actual configuration differs, or has drifted, from its expected configuration.',
                                                                                   input_parameters=None,  # Default: None
                                                                                   # Default: MaximumExecutionFrequency.TWENTY_FOUR_HOURS
                                                                                   maximum_execution_frequency=config.MaximumExecutionFrequency.ONE_HOUR,
                                                                                   # Default: - evaluations for the rule are triggered when any resource in the recording group changes.
                                                                                   rule_scope=None,
                                                                                   )
        cloudformation_drift_check.apply_removal_policy(removal_policy)

        CfnOutput(self, 'RuleArn',
                  description='The arn of the rule.',
                  value=cloudformation_drift_check.config_rule_arn,
                  )
        CfnOutput(self, 'ComplianceType',
                  description='The compliance status of the rule.',
                  value=cloudformation_drift_check.config_rule_compliance_type,
                  )
        CfnOutput(self, 'RuleId',
                  description='The id of the rule.',
                  value=cloudformation_drift_check.config_rule_id,
                  )
        CfnOutput(self, 'RuleName',
                  description='The name of the rule.',
                  value=cloudformation_drift_check.config_rule_name,
                  )

        topic = sns.Topic(self, "ComplianceTopic")
        topic.grant_publish(service_role)

        CfnOutput(self, 'ComplianceTopicArn', value=topic.topic_arn,)

        sns_target = targets.SnsTopic(topic)

        cloudformation_drift_check.on_compliance_change(
            'OnDrifted',
            description='The stack has drifted',
            rule_name='OnDrift',
            event_pattern=events.EventPattern(
                source=["aws.config"],
                detail_type=["Config Rules Compliance Change"],
                detail={
                    "configRuleName": ["CloudformationDriftDetectionRule"],
                    "newEvaluationResult": {
                        "complianceType": ["NON_COMPLIANT"]
                    }
                }
            ),
            target=sns_target,
        )
