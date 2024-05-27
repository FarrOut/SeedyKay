from aws_cdk import (
    # Duration,
    NestedStack, RemovalPolicy, aws_ec2 as ec2, aws_efs as efs, CfnOutput, )

from constructs import Construct


class EfsNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc,removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.file_system = efs.FileSystem(self, "Efs", vpc=vpc,
                                          removal_policy=removal_policy,
                                          )

        CfnOutput(self, 'FileSystemId',
                  description='The ID of the file system, assigned by Amazon EFS.',
                  value=str(self.file_system.file_system_id)
                  )
        CfnOutput(self, 'FileSystemArn',
                  description='The ARN of the file system.',
                  value=str(self.file_system.file_system_arn)
                  )