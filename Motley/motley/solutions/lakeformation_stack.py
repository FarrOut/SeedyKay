from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, aws_glue as glue, Aws, aws_s3 as s3, aws_iam as iam, aws_lakeformation as lakeformation, CfnOutput,
)
from constructs import Construct

from motley.components.analytics.lakeformation_nestedstack import LakeFormation
from motley.components.storage.block.s3_stack import S3NestedStack


class LakeFormationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = S3NestedStack(
            self, "S3NestedStack", removal_policy=removal_policy, auto_delete_objects=True,
            enforce_ssl=False,
        ).bucket

        self.role = iam.Role(self, "MyRole",
                        assumed_by=iam.ServicePrincipal(
                            "lakeformation.amazonaws.com"),
                        )
        self.role.apply_removal_policy(removal_policy)
        self.role.grant_assume_role(iam.ServicePrincipal(
            "glue.amazonaws.com"))
        # role.add_managed_policy(
        #     iam.ManagedPolicy.from_aws_managed_policy_name('LakeFormationDataAccessServiceRolePolicy'))
        self.role.add_to_policy(iam.PolicyStatement(
            sid='DatalakeUserBasic',
            effect=iam.Effect.ALLOW,
            actions=["lakeformation:*",
                     "cloudtrail:DescribeTrails",
                     "cloudtrail:LookupEvents",
                     "glue:GetDatabase",
                     "glue:GetDatabases",
                     "glue:CreateDatabase",
                     "glue:UpdateDatabase",
                     "glue:DeleteDatabase",
                     "glue:GetConnections",
                     "glue:SearchTables",
                     "glue:GetTable",
                     "glue:CreateTable",
                     "glue:UpdateTable",
                     "glue:DeleteTable",
                     "glue:GetTableVersions",
                     "glue:GetPartitions",
                     "glue:GetTables",
                     "glue:GetWorkflow",
                     "glue:ListWorkflows",
                     "glue:BatchGetWorkflows",
                     "glue:DeleteWorkflow",
                     "glue:GetWorkflowRuns",
                     "glue:StartWorkflowRun",
                     "glue:GetWorkflow",
                     "s3:ListBucket",
                     "s3:GetBucketLocation",
                     "s3:ListAllMyBuckets",
                     "s3:GetBucketAcl",
                     "iam:ListUsers",
                     "iam:ListRoles",
                     "iam:GetRole",
                     "iam:GetRolePolicy"],
            resources=["*"],
        ))

        resource = lakeformation.CfnResource(self, "MyCfnResource",
                                             resource_arn=bucket.bucket_arn,
                                             use_service_linked_role=True,

                                             # the properties below are optional
                                             #  role_arn=role.role_arn,
                                             with_federation=False,
                                             )
        resource.apply_removal_policy(removal_policy)

        CfnOutput(self, 'RoleArn', value=str(resource.role_arn),
                  description='The IAM role that registered a resource.')
        CfnOutput(self, 'ResourceArn', value=str(resource.resource_arn),
                  description='The Amazon Resource Name (ARN) of the resource.')

        self.database = glue.CfnDatabase(self, "MyCfnDatabase",
                                    catalog_id=Aws.ACCOUNT_ID,
                                    database_input=glue.CfnDatabase.DatabaseInputProperty(
                                        name="datalake-v5",
                                        description="datalake-v5",
                                    ))
        self.database.apply_removal_policy(removal_policy)


        lakeformation.CfnPrincipalPermissions(self, "DatabasePermissions",
                                              permissions=[
                                                  "CREATE_TABLE", "ALTER", "DESCRIBE"],
                                              permissions_with_grant_option=[],
                                              principal=lakeformation.CfnPrincipalPermissions.DataLakePrincipalProperty(
                                                  data_lake_principal_identifier=self.role.role_arn,
        ),
            resource=lakeformation.CfnPrincipalPermissions.ResourceProperty(
                                                  database=lakeformation.CfnPrincipalPermissions.DatabaseResourceProperty(
                                                      catalog_id=Aws.ACCOUNT_ID,
                                                      name=self.database.ref
                                                  ),
        ),
        )


   