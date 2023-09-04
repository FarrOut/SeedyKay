from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ecr as ecr, aws_ec2 as ec2, CfnOutput, RemovalPolicy, )
from constructs import Construct


class EcrRepoNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repository = ecr.Repository(self, "Repository",
                                    removal_policy=RemovalPolicy.DESTROY,
                                    )

        CfnOutput(self, 'RespositoryName',
                  description='The name of the repository.',
                  value=repository.repository_name
                  )
        CfnOutput(self, 'RespositoryArn',
                  description='The ARN of the repository.',
                  value=repository.repository_arn
                  )
        CfnOutput(self, 'RespositoryUri',
                  description='The URI of this repository (represents the latest image).',
                  value=repository.repository_uri
                  )
