from aws_cdk import (
    # Duration,
    aws_glue as glue, Stack, aws_iam as iam, CfnOutput, RemovalPolicy
)
from aws_cdk.aws_glue import CfnDatabase, CfnCrawler
from aws_cdk.aws_s3 import Bucket
from constructs import Construct


class GlueStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        crawler_role = iam.Role(self, 'SampleCrawlerRole',
                                assumed_by=iam.ServicePrincipal('glue.amazonaws.com'),
                                managed_policies=[
                                    iam.ManagedPolicy.from_aws_managed_policy_name(
                                        'service-role/AWSGlueServiceRole'),
                                    iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),
                                ])

        database = CfnDatabase(self, "MyCfnDatabase",
                               catalog_id=self.account,
                               database_input=CfnDatabase.DatabaseInputProperty(),
                               )

        CfnOutput(self, 'DatabaseName',
                  value=database.ref,
                  description='The database name.'
                  )

        bucket = Bucket(self, 'SourceBucket',
                        removal_policy=RemovalPolicy.DESTROY,
                        auto_delete_objects=True,
                        )

        crawler = CfnCrawler(self, 'SampleGlueCrawler',
                             role=crawler_role.role_arn,
                             database_name=database.ref,
                             targets=CfnCrawler.TargetsProperty(
                                 s3_targets=[
                                     CfnCrawler.S3TargetProperty(
                                         path=bucket.bucket_name,
                                     ),
                                 ],
                             ),
                             schedule=CfnCrawler.ScheduleProperty(
                                 schedule_expression="cron(* * * * *)",
                             )
                             )

        CfnOutput(self, 'CrawlerName',
                  value=crawler.ref,
                  description='The crawler name.'
                  )

        trigger = glue.CfnTrigger(self, "SampleGlueCrawlerTrigger",
                                  actions=[glue.CfnTrigger.ActionProperty(
                                      crawler_name=crawler.ref
                                  ), ],
                                  type="SCHEDULED",

                                  # the properties below are optional
                                  description="Trigger to run the crawler on creation to create necessary table",
                                  name="Sample_Glue_Crawler_Trigger",
                                  schedule="cron(* * * * *)",
                                  start_on_creation=True
                                  )

        CfnOutput(self, 'TriggerName',
                  value=trigger.ref,
                  description='The trigger name.'
                  )
