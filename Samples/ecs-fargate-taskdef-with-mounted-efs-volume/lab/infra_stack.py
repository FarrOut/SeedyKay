from aws_cdk import (
    # Duration,
    Stack,
    aws_efs as efs, CfnOutput,
    aws_ec2 as ec2, RemovalPolicy,
)
from aws_cdk.aws_efs import FileSystem
from constructs import Construct


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "VPC")

        self.file_system = efs.FileSystem(self, "MyEfsFileSystem",
                                          vpc=self.vpc,
                                          lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,
                                          # files are not transitioned to infrequent access (IA) storage by default
                                          performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
                                          removal_policy=RemovalPolicy.DESTROY,
                                          )
        self.file_system.apply_removal_policy(RemovalPolicy.DESTROY) # TODO debugging, set to RETAIN

        # CfnOutput(self, 'FileSystemArn',
        #           value=self.file_system.file_system_arn,
        #           description='The ARN of the file system.',
        #           )
        # CfnOutput(self, 'FileSystemId',
        #           value=self.file_system.file_system_id,
        #           description='The ID of the file system, assigned by Amazon EFS.',
        #           )
        # CfnOutput(self, 'VpcId',
        #           value=self.vpc.vpc_id,
        #           description='The ID of the VPC.',
        #           )
        
        self.security_group_id = ",".join(
            str(sg.security_group_id) for sg in self.file_system.connections.security_groups)
        CfnOutput(self, 'SecurityGroupId',
                  value=self.security_group_id,
                  description='The ID of the SecurityGroup.',
                  )
