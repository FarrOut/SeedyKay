from aws_cdk import (
    # Duration,
    aws_s3 as s3, aws_s3_deployment as s3deploy,
    NestedStack, RemovalPolicy, CfnOutput, )
from constructs import Construct

from motley.components.storage.block.s3_stack import S3NestedStack


class BucketDeploymentNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 auto_delete_objects: bool = False,
                 prune: bool = False,
                 exclude: [str] = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = S3NestedStack(self, 'S3NestedStack',
                                    removal_policy=removal_policy,
                                    auto_delete_objects=auto_delete_objects,
                                    ).bucket

        self.deployment = s3deploy.BucketDeployment(self, "DeployWebsite",
                                                    sources=[s3deploy.Source.asset(
                                                        "./assets/website-dist")],
                                                    destination_bucket=self.bucket,
                                                    destination_key_prefix="web/static",
                                                    retain_on_delete=auto_delete_objects,
                                                    prune=prune,
                                                    exclude=exclude,
                                                    )

        deployed_bucket = self.deployment.deployed_bucket

        CfnOutput(self, 'BucketArn',
                  description='The ARN of the bucket.',
                  value=deployed_bucket.bucket_arn,
                  )
        CfnOutput(self, 'BucketDomainName',
                  description='The IPv4 DNS name of the specified bucket.',
                  value=deployed_bucket.bucket_domain_name,
                  )
        CfnOutput(self, 'BucketName',
                  description='The name of the bucket.',
                  value=deployed_bucket.bucket_name,
                  )
        CfnOutput(self, 'BucketWebsiteUrl',
                  description='The URL of the static website.',
                  value=str(deployed_bucket.bucket_website_url),
                  )
        CfnOutput(self, 'BucketUri',
                  description='The Uri of the bucket.',
                  value=str('s3://{}'.format(deployed_bucket.bucket_name)),
                  )
