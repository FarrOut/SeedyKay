from aws_cdk import (
    # Duration,
    aws_cloudtrail as cloudtrail, aws_s3 as s3,
    NestedStack, RemovalPolicy, Duration, CfnOutput, )
from aws_cdk.aws_synthetics_alpha import Code, RuntimeFamily
from constructs import Construct

from motley.components.storage.block.s3_stack import S3NestedStack


class CloudTrailNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_one = S3NestedStack(self, 'BucketStackOne',
                                   removal_policy=removal_policy,
                                   auto_delete_objects=True,
                                   ).bucket
        bucket_two = S3NestedStack(self, 'BucketStackTwo',
                                   removal_policy=removal_policy,
                                   auto_delete_objects=True,
                                   ).bucket

        trail = cloudtrail.Trail(self, "CloudTrail",
                                 is_multi_region_trail=False,
                                 #  management_events=cloudtrail.ReadWriteType.WRITE_ONLY,
                                 )
        trail.apply_removal_policy(removal_policy)

        CfnOutput(self, 'TrailArn', value=trail.trail_arn,
                  description='ARN of the CloudTrail trail.')

        trail.add_s3_event_selector(
            s3_selector=[
                cloudtrail.S3EventSelector(
                    bucket=bucket_one, object_prefix=''),
                cloudtrail.S3EventSelector(bucket=bucket_two, object_prefix='')],
            read_write_type=cloudtrail.ReadWriteType.WRITE_ONLY,
            include_management_events=True,  # Default: True
        )

        trail.log_all_lambda_data_events(
            include_management_events=False,
        )
