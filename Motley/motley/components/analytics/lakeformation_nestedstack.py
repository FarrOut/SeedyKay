from aws_cdk import (
    # Duration,
    Aws,
    CfnTag, NestedStack, aws_lakeformation as lakeformation, aws_iam as iam, aws_glue as glue, aws_cloudtrail as cloudtrail, aws_s3 as s3,
    CfnOutput, RemovalPolicy, Duration, )
from constructs import Construct

from motley.components.storage.block.s3_stack import S3NestedStack


class LakeFormation(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = S3NestedStack(
            self, "S3NestedStack", removal_policy=removal_policy, auto_delete_objects=True,
            enforce_ssl=False,
        ).bucket

        # trail = cloudtrail.Trail(self, "CloudTrail",
        #                          bucket=bucket,
        #                          )
        # trail.apply_removal_policy(removal_policy)

        # CfnOutput(self, 'TrailArn', value=trail.trail_arn,
        #           description='Trail ARN')

        role = iam.Role(self, "MyRole",
                        assumed_by=iam.ServicePrincipal(
                            "lakeformation.amazonaws.com"),
                        )
        role.apply_removal_policy(removal_policy)
        role.grant_assume_role(iam.ServicePrincipal(
            "glue.amazonaws.com"))
        # role.add_managed_policy(
        #     iam.ManagedPolicy.from_aws_managed_policy_name('LakeFormationDataAccessServiceRolePolicy'))
        role.add_to_policy(iam.PolicyStatement(
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
        # bucket.grant_read_write(role)

        database = glue.CfnDatabase(self, "MyCfnDatabase",
                                    catalog_id=Aws.ACCOUNT_ID,
                                    database_input=glue.CfnDatabase.DatabaseInputProperty(
                                        name="datalake-v5",
                                        description="datalake-v5",
                                    ))
        database.apply_removal_policy(removal_policy)

        table_one = glue.CfnTable(self, "MyCfnTableOne",
                                  catalog_id=Aws.ACCOUNT_ID,
                                  database_name=database.ref,
                                  table_input=glue.CfnTable.TableInputProperty(

                                  ),
                                  )
        table_one.apply_removal_policy(removal_policy)

        table_two = glue.CfnTable(self, "MyCfnTableTwo",
                                  catalog_id=Aws.ACCOUNT_ID,
                                  database_name=database.ref,
                                  table_input=glue.CfnTable.TableInputProperty(
                                  ),
                                  )
        table_two.apply_removal_policy(removal_policy)

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

        # glue_db=glue.CfnDatabase(self, "GlueDatabase",
        #     catalog_id=Aws.ACCOUNT_ID,
        #     database_input=cdk.aws_glue.CfnDatabase.DatabaseInputProperty(
        #         name="datalake-v5",
        #         location_uri = s3_location
        #     )
        # )

        lakeformation.CfnPrincipalPermissions(self, "DatabasePermissions",
                                              permissions=[
                                                  "CREATE_TABLE", "ALTER", "DESCRIBE"],
                                              permissions_with_grant_option=[],
                                              principal=lakeformation.CfnPrincipalPermissions.DataLakePrincipalProperty(
                                                  data_lake_principal_identifier=role.role_arn,
                                              ),
                                              resource=lakeformation.CfnPrincipalPermissions.ResourceProperty(
                                                  database=lakeformation.CfnPrincipalPermissions.DatabaseResourceProperty(
                                                      catalog_id=Aws.ACCOUNT_ID,
                                                      name=database.ref
                                                  ),
                                              ),
                                              )

        # data_cells_filter = lakeformation.CfnDataCellsFilter(self, "MyCfnDataCellsFilter",
        #                                                      database_name=database.ref,
        #                                                      name="table-one-data-cell",
        #                                                      table_catalog_id=Aws.ACCOUNT_ID,
        #                                                      table_name=table_one.ref,
        #                                                      row_filter=lakeformation.CfnDataCellsFilter.RowFilterProperty(
        #                                                          all_rows_wildcard={},
        #                                                          #  filter_expression="filterExpression"
        #                                                      ),
        #                                                      column_wildcard=lakeformation.CfnDataCellsFilter.ColumnWildcardProperty(
        #                                                          # excluded_column_names=["excludedColumnNames"]
        #                                                      ),
        #                                                      )

        # lakeformation.CfnPrincipalPermissions(self, "DataCellsFilterPermissions",
        #                                       permissions=[
        #                                           "SELECT"],
        #                                       permissions_with_grant_option=[],
        #                                       principal=lakeformation.CfnPrincipalPermissions.DataLakePrincipalProperty(
        #                                           data_lake_principal_identifier=role.role_arn,
        #                                       ),
        #                                       resource=lakeformation.CfnPrincipalPermissions.ResourceProperty(
        #                                           data_cells_filter=lakeformation.CfnPrincipalPermissions.DataCellsFilterResourceProperty(
        #                                               database_name=database.ref,
        #                                               name="table-one-data-cell",
        #                                               table_catalog_id=Aws.ACCOUNT_ID,
        #                                               table_name=table_one.ref
        #                                           ),
        #                                       ),
        #                                       )

        lakeformation.CfnPrincipalPermissions(self, "TableOnePermissions",
                                              permissions=[
                                                  "SELECT"],
                                              permissions_with_grant_option=[],
                                              principal=lakeformation.CfnPrincipalPermissions.DataLakePrincipalProperty(
                                                  data_lake_principal_identifier=role.role_arn,
                                              ),
                                              resource=lakeformation.CfnPrincipalPermissions.ResourceProperty(
                                                  table=lakeformation.CfnPrincipalPermissions.TableResourceProperty(
                                                      catalog_id=Aws.ACCOUNT_ID,
                                                      database_name=database.ref,
                                                      name=table_one.ref
                                                  ),
                                              ),
                                              )

        lakeformation.CfnPrincipalPermissions(self, "TableTwoPermissions",
                                              permissions=["SELECT"],
                                              permissions_with_grant_option=[],
                                              principal=lakeformation.CfnPrincipalPermissions.DataLakePrincipalProperty(
                                                  data_lake_principal_identifier=role.role_arn,
                                              ),
                                              resource=lakeformation.CfnPrincipalPermissions.ResourceProperty(
                                                  table=lakeformation.CfnPrincipalPermissions.TableResourceProperty(
                                                      catalog_id=Aws.ACCOUNT_ID,
                                                      database_name=database.ref,
                                                      name=table_two.ref
                                                  ),
                                              ),
                                              )

        database_two = glue.CfnDatabase(self, "MyCfnDatabaseTwo",
                                        catalog_id=Aws.ACCOUNT_ID,
                                        database_input=glue.CfnDatabase.DatabaseInputProperty(
                                            name="datalake-v5-2",
                                            description="datalake-v5-2",
                                        ))
        database_two.apply_removal_policy(removal_policy)

        db_two_table_one = glue.CfnTable(self, "DbOneTableOne",
                                         catalog_id=Aws.ACCOUNT_ID,
                                         database_name=database_two.ref,
                                         table_input=glue.CfnTable.TableInputProperty(),
                                         )
        db_two_table_one.apply_removal_policy(removal_policy)

        db_two_table_two = glue.CfnTable(self, "DbOneTableTwo",
                                         catalog_id=Aws.ACCOUNT_ID,
                                         database_name=database_two.ref,
                                         table_input=glue.CfnTable.TableInputProperty(),
                                         )
        db_two_table_two.apply_removal_policy(removal_policy)

        lakeformation.CfnPrincipalPermissions(self, "DatabaseTwoPermissions",
                                              permissions=[
                                                  "CREATE_TABLE",  "DROP", "DESCRIBE"],
                                              permissions_with_grant_option=[],
                                              principal=lakeformation.CfnPrincipalPermissions.DataLakePrincipalProperty(
                                                  data_lake_principal_identifier=role.role_arn,
                                              ),
                                              resource=lakeformation.CfnPrincipalPermissions.ResourceProperty(
                                                  database=lakeformation.CfnPrincipalPermissions.DatabaseResourceProperty(
                                                      catalog_id=Aws.ACCOUNT_ID,
                                                      name=database_two.ref
                                                  ),
                                              ),
                                              )

        lakeformation.CfnPrincipalPermissions(self, "DbOneTableOnePermissions",
                                              permissions=[
                                                  "SELECT", "DESCRIBE"],
                                              permissions_with_grant_option=[],
                                              principal=lakeformation.CfnPrincipalPermissions.DataLakePrincipalProperty(
                                                  data_lake_principal_identifier=role.role_arn,
                                              ),
                                              resource=lakeformation.CfnPrincipalPermissions.ResourceProperty(
                                                  table=lakeformation.CfnPrincipalPermissions.TableResourceProperty(
                                                      catalog_id=Aws.ACCOUNT_ID,
                                                      database_name=database_two.ref,
                                                      name=db_two_table_one.ref
                                                  ),
                                              ),
                                              )

        lakeformation.CfnPrincipalPermissions(self, "DbOneTableTwoPermissions",
                                              permissions=["DESCRIBE"],
                                              permissions_with_grant_option=[],
                                              principal=lakeformation.CfnPrincipalPermissions.DataLakePrincipalProperty(
                                                  data_lake_principal_identifier=role.role_arn,
                                              ),
                                              resource=lakeformation.CfnPrincipalPermissions.ResourceProperty(
                                                  table=lakeformation.CfnPrincipalPermissions.TableResourceProperty(
                                                      catalog_id=Aws.ACCOUNT_ID,
                                                      database_name=database_two.ref,
                                                      name=db_two_table_two.ref
                                                  ),
                                              ),
                                              )
