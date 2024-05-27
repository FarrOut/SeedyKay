from aws_cdk import (
    # Duration,
    NestedStack, RemovalPolicy, CfnOutput, aws_iam as iam, aws_guardduty as guardduty,
)
from aws_cdk.aws_kms import Key

from constructs import Construct


class GuardDutyNest(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        data_sources = guardduty.CfnDetector.CFNDataSourceConfigurationsProperty(
            malware_protection=guardduty.CfnDetector.CFNMalwareProtectionConfigurationProperty(
                scan_ec2_instance_with_findings=guardduty.CfnDetector.CFNScanEc2InstanceWithFindingsConfigurationProperty(
                    ebs_volumes=False
                )
            ), s3_logs=guardduty.CfnDetector.CFNS3LogsConfigurationProperty(
                enable=True
            ), kubernetes=guardduty.CfnDetector.CFNKubernetesConfigurationProperty(
                audit_logs=guardduty.CfnDetector.CFNKubernetesAuditLogsConfigurationProperty(
                    enable=False
                )
            ),
        )

        features = [guardduty.CfnDetector.CFNFeatureConfigurationProperty(
            name="name",
            status="ENABLED", # Allowed values: ENABLED | DISABLED

            # the properties below are optional
            # additional_configuration=[guardduty.CfnDetector.CFNFeatureAdditionalConfigurationProperty(
            #     name="name",
            #     status="ENABLED"
            # )]
        )]

        # Make sure you use either DataSources or Features in a one request, and not both.
        #
        # @see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#aws-resource-guardduty-detector--examples

        detector = guardduty.CfnDetector(self, "MyCfnDetector",
                                         enable=True,
                                        #  data_sources=data_sources,
                                         features=features,
                                         )
        detector.apply_removal_policy(removal_policy)

        CfnOutput(self, "GuardDutyDetectorId", value=detector.attr_id)
        CfnOutput(self, "GuardDutyDetectorEnabled", value=str(detector.enable))
