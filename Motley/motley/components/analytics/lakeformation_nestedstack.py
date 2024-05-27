from aws_cdk import (
    # Duration,
    Aws, PhysicalName,
    CfnTag, Stack, aws_lakeformation as lakeformation, aws_iam as iam, aws_glue as glue, aws_cloudtrail as cloudtrail, aws_s3 as s3,
    CfnOutput, RemovalPolicy, Duration, )
from constructs import Construct

from motley.components.storage.block.s3_stack import S3NestedStack


class LakeFormation(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 identifier: str,
                 database: glue.CfnDatabase,
                 role: iam.IRole,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

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



        lakeformation.CfnPrincipalPermissions(self, f"TableOnePermissions-{identifier}",
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

        lakeformation.CfnPrincipalPermissions(self, f"TableTwoPermissions-{identifier}",
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
