from aws_cdk import (core as cdk,
                     aws_ec2 as ec2,
                     )
import os

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class NewPrivateSubnetsInExistingVpcStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lookup existing, default Vpc
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Vpc.html#aws_cdk.aws_ec2.Vpc.from_lookup
        # CIDR = 172.31.0.0/16
        vpc_ = ec2.Vpc.from_lookup(self, 'DefaultVpc',
                                   is_default=True,
                                   )

        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Subnet.html
        subnet_priv_a_ = ec2.Subnet(self, 'PrivateNetA',
                                    availability_zone=vpc_.availability_zones[0],
                                    map_public_ip_on_launch=True,
                                    vpc_id=vpc_.vpc_id,
                                    cidr_block='172.31.11.0/24',
                                    )

        subnet_priv_b_ = ec2.Subnet(self, 'PrivateNetB',
                                    availability_zone=vpc_.availability_zones[1],
                                    map_public_ip_on_launch=True,
                                    vpc_id=vpc_.vpc_id,
                                    cidr_block='172.31.22.0/24',
                                    )
