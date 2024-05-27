from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ecr as ecr, aws_ec2 as ec2, CfnOutput, RemovalPolicy, )
from aws_cdk.aws_ecs import ContainerImage, RepositoryImage
from aws_cdk.aws_secretsmanager import ISecret
from aws_cdk.aws_sns import Topic
from constructs import Construct


class EcrImageNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, image_name: str, credentials: ISecret = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.image: RepositoryImage = ContainerImage.from_registry(image_name, credentials=credentials)

        CfnOutput(self, 'isImageNull', value=str(self.image is None), description='is the image null.')

        if credentials is not None:
            CfnOutput(self, 'SecretName', value=credentials.secret_name,
                      description='The name of the Secret resource.')
            CfnOutput(self, 'SecretFullArn', value=credentials.secret_full_arn,
                      description='The full ARN of the Secret resource.')
            CfnOutput(self, 'SecretArn', value=credentials.secret_arn,
                      description='The ARN of the Secret resource.')

            # ### How to resolve SecretValue ###
            # secret_value = str(credentials.secret_value_from_json("password").unsafe_unwrap())
            #
            # dummy = Topic(self, 'Dummy',
            #               topic_name=secret_value,
            #               )
            # CfnOutput(self, 'SecretValue',
            #           description='Resolved secret value',
            #           value=dummy.topic_name
            #           )

        # CfnOutput(self, "ImageName", value=str(self.image.image_name),
        #           description="Specifies the name of the container image.")
        # CfnOutput(self, "ImageRepositoryCredentials", value=str(self.image.repository_credentials),
        #           description="Specifies the credentials used to access the image repository.")
