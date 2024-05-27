from aws_cdk import (
    # Duration,
    NestedStack, aws_cloudfront as cloudfront, aws_cloudfront_origins as origins, aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    RemovalPolicy, aws_elasticloadbalancingv2 as elbv2, aws_ec2 as ec2, CfnOutput, )
from constructs import Construct


class CloudFrontNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, web_acl_id: str = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        storage = self.Storage(self, 'StorageNestedStack', removal_policy=removal_policy)

        distro = cloudfront.Distribution(self, "myDist",
                                         default_behavior=cloudfront.BehaviorOptions(
                                             origin=origins.S3Origin(storage.origin_bucket)),
                                         log_bucket=storage.log_bucket,
                                         log_file_prefix="distribution-access-logs/",
                                         log_includes_cookies=True,
                                         web_acl_id=web_acl_id,
                                         )
        distro.apply_removal_policy(removal_policy)

    class Storage(NestedStack):

        def __init__(self, scope: Construct, construct_id: str, removal_policy: RemovalPolicy, **kwargs) -> None:
            super().__init__(scope, construct_id, **kwargs)

            self.log_bucket = s3.Bucket(self, "CloudFrontLoggingBucket",
                                        removal_policy=removal_policy,
                                        auto_delete_objects=True,
                                        block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                        object_ownership=s3.ObjectOwnership.OBJECT_WRITER,
                                        encryption=s3.BucketEncryption.S3_MANAGED,
                                        )

            self.origin_bucket = s3.Bucket(self, "CloudFrontOriginBucket",
                                           removal_policy=removal_policy,
                                           auto_delete_objects=True,
                                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                           object_ownership=s3.ObjectOwnership.OBJECT_WRITER,
                                           encryption=s3.BucketEncryption.S3_MANAGED,
                                           website_index_document="index.html",
                                           )
            s3deploy.BucketDeployment(self, "DeployWebsite",
                                      sources=[s3deploy.Source.asset("./assets/website-dist")],
                                      destination_bucket=self.origin_bucket,
                                      destination_key_prefix="web/static"
                                      )
