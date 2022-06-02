from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2, CfnOutput,
)
from constructs import Construct


class VanillaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, 'DefaultVpc')

        CfnOutput(self, 'VpcId',
                  description='Identifier for this VPC.',
                  value=vpc.vpc_id,
                  )

        CfnOutput(self, 'Vpc',
                  description='Arn of this VPC.',
                  value=vpc.vpc_arn,
                  )

        CfnOutput(self, 'PrivateSubnets',
                  description='List of private subnets in this VPC.',
                  value=str([s.subnet_id for s in vpc.private_subnets]),
                  )

        CfnOutput(self, 'IsolatedSubnets',
                  description='List of isolated subnets in this VPC.',
                  value=str([s.subnet_id for s in vpc.isolated_subnets]),
                  )

        CfnOutput(self, 'PublicSubnets',
                  description='List of public subnets in this VPC.',
                  value=str([s.subnet_id for s in vpc.public_subnets]),
                  )

        CfnOutput(self, 'AvailabilityZones',
                  description='AZs for this VPC.',
                  value=str(vpc.availability_zones),
                  )
