from aws_cdk import (
    # Duration,
    NestedStack, RemovalPolicy, CfnOutput, aws_inspector as inspector,
)
from aws_cdk.aws_kms import Key

from constructs import Construct


class InspectorClassicNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 assessment_target_name: str = None,
                 resource_group_arn: str = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        assessment_target = inspector.CfnAssessmentTarget(self, "MyAssessmentTarget",
                                                          assessment_target_name=assessment_target_name,
                                                          resource_group_arn=resource_group_arn,
                                                          )
        assessment_target.apply_removal_policy(removal_policy)

        CfnOutput(self, "AssessmentTargetArn",
                  value=str(assessment_target.attr_arn),
                  description='The Amazon Resource Name (ARN) that specifies the assessment target that is created.')
        CfnOutput(self, "AssessmentTargetName",
                  value=str(assessment_target.assessment_target_name),
                  description='The name of the Amazon Inspector assessment target.')
        CfnOutput(self, "ResourceGroupArn",
                  value=str(assessment_target.resource_group_arn),
                  description='The ARN that specifies the resource group that is used to create the assessment target.')
