from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy,aws_s3 as s3, )
from constructs import Construct
from motley.components.orchestration.service_catalog_nestedstack import ServiceCatalogNestedStack


class ServiceCatalogStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "TheresAHoleInMyBucket",
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                           enforce_ssl=True,
                           versioned=True,
                           auto_delete_objects=True,
                           removal_policy=RemovalPolicy.DESTROY,
                           ),

        ServiceCatalogNestedStack(
            self, "ServiceCatalogNestedStack", removal_policy=removal_policy, asset_bucket=bucket,)
