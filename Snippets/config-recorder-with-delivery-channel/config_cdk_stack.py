from aws_cdk import (
    # Duration,
    Stack,
    aws_config as config,
    aws_iam as iam,
    aws_s3 as s3,
)
from aws_cdk.aws_iam import Role, ServicePrincipal, PolicyStatement, Effect
from constructs import Construct


class ConfigCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        config_iam_role = Role(self, "MyRole",
                               assumed_by=ServicePrincipal("config.amazonaws.com"),
                               managed_policies=[
                                   iam.ManagedPolicy.from_aws_managed_policy_name(
                                       'service-role/AWSConfigRole')
                               ],
                               )

        bucket = s3.Bucket(self, "MyFirstBucket")
        # Attaches the AWSConfigBucketPermissionsCheck policy statement.
        bucket.add_to_resource_policy(
            PolicyStatement(
                effect=Effect.ALLOW,
                principals=[config_iam_role],
                resources=[bucket.bucket_arn],
                actions=['s3:GetBucketAcl'],
            )
        )

        # Attaches the AWSConfigBucketDelivery policy statement.
        bucket.add_to_resource_policy(
            PolicyStatement(
                effect=Effect.ALLOW,
                principals=[config_iam_role],
                resources=[bucket.arn_for_objects('AWSLogs/' + self.account + '/Config/*')],
                actions=['s3:PutObject'],
                conditions={
                    'StringEquals': {
                        's3:x-amz-acl': 'bucket-owner-full-control',
                    },
                },
            )
        )

        ## CONFIG CONFIGURATION RECORDER
        config_configuration_recorder = config.CfnConfigurationRecorder(self, "ConfigConfigurationRecorder",
                                                                        role_arn=config_iam_role.role_arn,
                                                                        recording_group=config.CfnConfigurationRecorder.RecordingGroupProperty(
                                                                            all_supported=True,
                                                                            include_global_resource_types=False
                                                                        )
                                                                        )

        ## CONFIG DELIVERY CHANNEL
        config_delivery_channel = config.CfnDeliveryChannel(self, "ConfigDeliveryChannel",
                                                            config_snapshot_delivery_properties=config.CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty(
                                                                delivery_frequency="TwentyFour_Hours"
                                                            ),
                                                            s3_bucket_name=bucket.bucket_name,
                                                            )

        cfn_config_rule = config.CfnConfigRule(self, "MyCfnConfigRule",
                                               config_rule_name='cloudtrail-enabled',
                                               source=config.CfnConfigRule.SourceProperty(
                                                   owner="AWS",
                                                   source_identifier="CLOUD_TRAIL_ENABLED",
                                               ),
                                               )
