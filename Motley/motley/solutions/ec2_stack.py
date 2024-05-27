from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2, aws_iot as iot,
    RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_ecs import ContainerImage
from constructs import Construct

from motley.components.computing.launch_template_nestedstack import LaunchTemplateNestedStack
from motley.components.computing.simple_instance_nestedstack import SimpleInstanceNestedStack
from motley.components.computing.encrypted_instance_nestedstack import EncryptedInstanceNestedStack

class Ec2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.IVpc,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # LaunchTemplateNestedStack(self, 'LaunchTemplateNestedStack',
        #                removal_policy=removal_policy,
        #                vpc=vpc,
        #                )

        # SimpleInstanceNestedStack(self, 'SimpleInstanceNestedStack',
        #                           removal_policy=removal_policy,
        #                           vpc=vpc,
        #                           )

        EncryptedInstanceNestedStack(self, 'EncryptedInstanceNestedStack',
                                  removal_policy=removal_policy,
                                  vpc=vpc,
                                  )