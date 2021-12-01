from aws_cdk import (
    core as cdk,
    aws_nimblestudio as nimblestudio,
    aws_iam as iam,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk.aws_iam import ServicePrincipal, ManagedPolicy


class NimblestudioStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        admin_role = iam.Role(self, "AdminRole",
                              assumed_by=ServicePrincipal('identity.nimble.eu-west-2.amazonaws.com'),
                              description="This is the admin role.",
                              managed_policies=[
                                  ManagedPolicy.from_aws_managed_policy_name('AmazonNimbleStudio-StudioAdmin')],
                              )
        user_role = iam.Role(self, "UserRole",
                             assumed_by=ServicePrincipal('identity.nimble.eu-west-2.amazonaws.com'),
                             description="This is the user role.",
                             managed_policies=[
                                 ManagedPolicy.from_aws_managed_policy_name('AmazonNimbleStudio-StudioUser')],
                             )

        studio = nimblestudio.CfnStudio(self, "MyNimbleStudio",
                                        admin_role_arn=admin_role.role_arn,
                                        display_name="The Nimble Studio",

                                        # Your studio name must be between 3-64 characters and only include lowercase letters from a-z and numbers from 0-9.
                                        # https://docs.aws.amazon.com/nimble-studio/latest/userguide/deploy-studio.html#deploying-a-new-studio-step-4
                                        studio_name="thenimblestudio",
                                        user_role_arn=user_role.role_arn,

                                        tags={
                                            "Name": "TheNimbleStudio"
                                        }
                                        )
