from aws_cdk import (
    # Duration,
    NestedStack, aws_sagemaker_alpha as sagemaker,
    RemovalPolicy, CfnOutput, )
from constructs import Construct


class SageMakerSingleModelNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, repo_name: str, image_tag: str, account_id: str = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DLC Available Image User Guide
        # https://github.com/aws/deep-learning-containers/blob/master/available_images.md#dlc-available-image-user-guide
        image = sagemaker.ContainerImage.from_dlc(
            repository_name=repo_name,
            tag=image_tag,
            account_id=account_id,
        )

        model_data = None

        model = sagemaker.Model(self, "PrimaryContainerModel",
                                containers=[sagemaker.ContainerDefinition(
                                    image=image,
                                    model_data=model_data
                                )
                                ]
                                )
        # model.apply_removal_policy(removal_policy)

        CfnOutput(self, 'ModelName', value=model.model_name, description='The name of the model.')
        CfnOutput(self, 'ModelArn', value=model.model_arn, description='The ARN of the model.')
        CfnOutput(self, 'ModelRoleArn', value=model.role.role_arn, description='The ARN of the model\'s role.')
        CfnOutput(self, 'ModelGrantPrincipalArn', value=model.grant_principal.role_arn,
                  description='The principal this Model is running as.')
