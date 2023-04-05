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

        cluster = rds.DatabaseCluster(self, "Database",
                                      engine=rds.DatabaseClusterEngine.aurora_postgres(
                                          version=rds.AuroraPostgresEngineVersion.VER_13_7),
                                      credentials=rds.Credentials.from_generated_secret("clusteradmin"),
                                      # Optional - will default to 'admin' username and generated password
                                      instance_props=rds.InstanceProps(
                                          # optional , defaults to t3.medium
                                          instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5,
                                                                            ec2.InstanceSize.LARGE),
                                          vpc_subnets=ec2.SubnetSelection(
                                              subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                                          ),
                                          vpc=vpc
                                      )
                                      )
