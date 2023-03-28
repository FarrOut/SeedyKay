from aws_cdk import (core as cdk,
                     aws_ec2 as ec2,
                     )
from aws_cdk.aws_ec2 import SubnetConfiguration, SubnetType

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class DemoStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Number of Subnets pairs to create, this will create n-number of Public and Private Subnets
        subnet_count = 2

        # Define the maximum number of AZs to use in this region.
        az_count = 3

        # Build array of Subnet configs to pass to VPC
        subnet_config = []
        for x in range(subnet_count):
            print('Adding subnet ' + str(x))
            subnet_config.append(SubnetConfiguration(
                name='Subnet' + str(x),
                subnet_type=SubnetType.PUBLIC,
            ))

        # Create VPC with desired Subnets
        vpc = ec2.Vpc(self, "TheVPC",
                      cidr="10.112.0.0/16",
                      subnet_configuration=subnet_config,
                      max_azs=az_count,
                      )
