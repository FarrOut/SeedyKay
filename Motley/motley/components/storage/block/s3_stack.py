from aws_cdk import (
    # Duration,
    aws_s3 as s3,
    NestedStack, RemovalPolicy, CfnOutput, )
from constructs import Construct


class S3NestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 bucket_name: str = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 enforce_ssl: bool = True,
                 auto_delete_objects: bool = False,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = s3.Bucket(self, "TheresAHoleInMyBucket",
                                bucket_name=bucket_name,
                                block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                encryption=s3.BucketEncryption.S3_MANAGED,
                                enforce_ssl=enforce_ssl,
                                versioned=True,
                                auto_delete_objects=auto_delete_objects,
                                removal_policy=removal_policy,
                                )

        CfnOutput(self, 'BucketArn',
                  description='The ARN of the bucket.',
                  value=self.bucket.bucket_arn,
                  )
        CfnOutput(self, 'BucketDomainName',
                  description='The IPv4 DNS name of the specified bucket.',
                  value=self.bucket.bucket_domain_name,
                  )
        CfnOutput(self, 'BucketName',
                  description='The name of the bucket.',
                  value=self.bucket.bucket_name,
                  )
        CfnOutput(self, 'BucketWebsiteUrl',
                  description='The URL of the static website.',
                  value=str(self.bucket.bucket_website_url),
                  )
        CfnOutput(self, 'BucketUri',
                  description='The Uri of the bucket.',
                  value=str('s3://{}'.format(self.bucket.bucket_name)),
                  )
