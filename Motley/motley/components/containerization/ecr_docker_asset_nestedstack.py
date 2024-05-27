from aws_cdk import (
    # Duration,
    NestedStack, aws_ecr_assets as ecr_assets,IgnoreMode,
    aws_ecr as ecr, aws_ec2 as ec2, CfnOutput, RemovalPolicy, )
from aws_cdk.aws_ecs import ContainerImage, RepositoryImage
from aws_cdk.aws_secretsmanager import ISecret
from aws_cdk.aws_sns import Topic
from constructs import Construct
from os import path


class EcrDockerAssetNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        asset = ecr_assets.DockerImageAsset(self, "GoLangImage",
                                            directory=path.join(
                                                'assets/containers/', "GoLang"),
                                            ignore_mode=IgnoreMode.DOCKER,
                                            )

        CfnOutput(self, 'AssetHash',
                  value=asset.asset_hash,
                  description='Asset Hash')
        CfnOutput(self, 'ImageTag',
                  value=asset.image_tag,
                  description='Image Tag')
        CfnOutput(self, 'ImageUri', value=asset.image_uri,
                  description='Image URI')
