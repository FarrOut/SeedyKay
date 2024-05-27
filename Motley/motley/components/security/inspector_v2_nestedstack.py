from aws_cdk import (
    # Duration,
    NestedStack, PhysicalName, RemovalPolicy, CfnOutput, aws_inspectorv2 as inspectorv2,
)
from aws_cdk.aws_kms import Key

from constructs import Construct


class InspectorV2NestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 filter_action: str,
                 filter_name: str = PhysicalName.GENERATE_IF_NEEDED,
                 filter_criteria: [inspectorv2.CfnFilter.FilterCriteriaProperty] = [],
                 description: str = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        filter = inspectorv2.CfnFilter(self, "MyCfnFilter",
                                       name=filter_name,
                                       filter_action=filter_action,
                                       filter_criteria=filter_criteria,
                                       description=description,
                                       )
