from aws_cdk import (
    # Duration,
    PhysicalName, Stack, RemovalPolicy, aws_kms as kms, CfnStackSet, aws_s3_deployment as s3deploy, Fn, CfnTag,
)
from constructs import Construct

from motley.components.storage.block.s3_stack import S3NestedStack


class StackSetsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 deployment_ou_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = S3NestedStack(self, 'S3NestedStack',
                                    removal_policy=removal_policy,
                                    auto_delete_objects=True,
                                    bucket_name=PhysicalName.GENERATE_IF_NEEDED,
                                    ).bucket

        self.deployment = s3deploy.BucketDeployment(self, "DeployWebsite",
                                                    sources=[s3deploy.Source.asset(
                                                        "./assets/stacksets")],
                                                    destination_bucket=self.bucket,
                                                    destination_key_prefix="stacksets",
                                                    retain_on_delete=False,
                                                    )

        deployed_bucket = self.deployment.deployed_bucket

        cfn_stack_set = CfnStackSet(self, "MyCfnStackSet",
                                    permission_model="SERVICE_MANAGED",
                                    stack_set_name='myTestStackSet',

                                    # the properties below are optional
                                    # administration_role_arn="administrationRoleArn",
                                    auto_deployment=CfnStackSet.AutoDeploymentProperty(
                                        enabled=True,
                                        retain_stacks_on_account_removal=False
                                    ),

                                    managed_execution={"Active": True},
                                    operation_preferences=CfnStackSet.OperationPreferencesProperty(
                                        failure_tolerance_percentage=0,
                                        max_concurrent_percentage=50,
                                        region_concurrency_type="parallel",
                                    ),
                                    stack_instances_group=[CfnStackSet.StackInstancesProperty(
                                        deployment_targets=CfnStackSet.DeploymentTargetsProperty(
                                            organizational_unit_ids=[
                                                deployment_ou_id]
                                        ),
                                        regions=["eu-west-1",
                                                 "us-east-1",
                                                 "ap-southeast-2"],
                                    )],
                                    tags=[CfnTag(
                                        key="Origin",
                                        value=self.stack_name
                                    )],
                                    template_url=Fn.select(
                                        0, self.deployment.object_keys),)
