from aws_cdk import (
    # Duration,
    Stack,
    aws_rds as rds,
    aws_ec2 as ec2,
)
from constructs import Construct


class RdsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC")

        instance = rds.DatabaseInstance(self, "Instance",
                                        engine=rds.DatabaseInstanceEngine.postgres(
                                            version=rds.PostgresEngineVersion.VER_14_2),
                                        # optional, defaults to m5.large
                                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5,
                                                                          ec2.InstanceSize.LARGE),
                                        credentials=rds.Credentials.from_generated_secret("syscdk"),
                                        # Optional - will default to 'admin' username and generated password
                                        vpc=vpc,
                                        vpc_subnets=ec2.SubnetSelection(
                                            subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
                                        )
                                        )
