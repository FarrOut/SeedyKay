from aws_cdk import (
    # Duration,
    NestedStack, RemovalPolicy, CfnOutput, aws_config as config, aws_iam as iam, aws_events_targets as targets, aws_sns as sns, aws_events as events,
)

from constructs import Construct

from motley.components.security.compliance.config_rules_nestedstack import ConfigRulesNestedStack


class ConfigNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(self, "ConfigServiceRole",
                        assumed_by=iam.ServicePrincipal("config.amazonaws.com")
                        )
        role.apply_removal_policy(removal_policy)
        # role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
        #     'AWSConfigRulesExecutionRole'))
        # TODO add required permissions (PutEvaulations)
        # https://docs.aws.amazon.com/config/latest/developerguide/security-iam-awsmanpol.html

        # role.add_managed_policy(iam.ManagedPolicy.from_managed_policy_arn(self, 'AWSConfigServiceRolePolicy',
        #                                                                   managed_policy_arn='arn:aws:iam::aws:policy/aws-service-role/AWSConfigServiceRolePolicy'))
        role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=['config:PutEvaluations'],
            resources=['*']
        ))
        CfnOutput(self, 'ConfigRoleArn', value=role.role_arn)

        recorder = config.CfnConfigurationRecorder(self, 'ConfigRecorder',
                                                   name='MyConfigRecorder',
                                                   role_arn=role.role_arn,
                                                   recording_group=config.CfnConfigurationRecorder.RecordingGroupProperty(
                                                       all_supported=False,
                                                       #    exclusion_by_resource_types=config.CfnConfigurationRecorder.ExclusionByResourceTypesProperty(
                                                       #        resource_types=[
                                                       #            "resourceTypes"]
                                                       #    ),
                                                       include_global_resource_types=False,
                                                       recording_strategy=config.CfnConfigurationRecorder.RecordingStrategyProperty(
                                                           use_only="INCLUSION_BY_RESOURCE_TYPES"
                                                       ),
                                                       resource_types=[
                                                           "AWS::CloudFormation::Stack", "AWS::Lambda::Function", "AWS::SNS::Topic", "AWS::EC2::Instance", "AWS::IAM::User", "AWS::IAM::Role", "AWS::IAM::Policy"]
                                                   ),
                                                   recording_mode=config.CfnConfigurationRecorder.RecordingModeProperty(
                                                       recording_frequency="DAILY",

                                                       # the properties below are optional
                                                       recording_mode_overrides=[config.CfnConfigurationRecorder.RecordingModeOverrideProperty(
                                                           recording_frequency="CONTINUOUS",
                                                           resource_types=[
                                                               "AWS::CloudFormation::Stack", "AWS::Lambda::Function", "AWS::SNS::Topic"],

                                                           # the properties below are optional
                                                           description="Just for testing, let us scan quickly"
                                                       )]
                                                   )
                                                   )
        recorder.apply_removal_policy(removal_policy)

        rule_stack = ConfigRulesNestedStack(self, 'ConfigRulesNestedStack',
                                            service_role=role,
                                            removal_policy=removal_policy,
                                            )
