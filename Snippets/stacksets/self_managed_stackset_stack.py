import os
from os import path

from aws_cdk import (
    # Duration,
    Stack, CfnStackSet, CfnTag,
    aws_s3_assets as assets, CfnOutput,
)
from aws_cdk.aws_s3_assets import Asset
from constructs import Construct


class ReproStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dirname = os.path.dirname(__file__)

        template_asset = Asset(self, 'DummyTemplate',
                               path=os.path.join(dirname, './template.yaml')
                               )

        CfnOutput(self, "S3BucketName", value=template_asset.s3_bucket_name)
        CfnOutput(self, "S3ObjectKey", value=template_asset.s3_object_key)
        CfnOutput(self, "S3HttpURL", value=template_asset.http_url)
        CfnOutput(self, "S3ObjectURL", value=template_asset.s3_object_url)

        stack_set = CfnStackSet(self, 'MyStackSet',
                                stack_set_name='SetOfStacks',
                                capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_IAM'],
                                description='',
                                tags=[CfnTag(
                                    key="Name",
                                    value="Self-Managed stacksets"
                                )],
                                template_url=template_asset.http_url,
                                stack_instances_group=[CfnStackSet.StackInstancesProperty(
                                    deployment_targets=CfnStackSet.DeploymentTargetsProperty(
                                        accounts=[
                                            "xxxxxxxxxxx",  # Master
                                        ],
                                    ),
                                    regions=["eu-west-1"],
                                )],
                                permission_model='SELF_MANAGED',
                                )
