from aws_cdk import (
    # Duration,
    Stack,
    aws_fsx as fsx, CfnOutput,
    aws_ec2 as ec2,
)
from constructs import Construct


class FsxStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        file_system = fsx.LustreFileSystem(self, "FsxLustreFileSystem",
                                           lustre_configuration=fsx.LustreConfiguration(
                                               deployment_type=fsx.LustreDeploymentType.SCRATCH_2),
                                           storage_capacity_gib=1200,
                                           vpc=vpc,
                                           vpc_subnet=vpc.private_subnets[0]
                                           )

        CfnOutput(self, 'FyleSystemId', value=file_system.file_system_id,
                  description='The ID that AWS assigns to the file system.'
                  )
