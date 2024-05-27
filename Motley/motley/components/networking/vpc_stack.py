import logging

from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ec2 as ec2, CfnOutput, RemovalPolicy, )
from constructs import Construct


class VpcNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        log = logging.getLogger()

        log.info("Creating new VPC")
        self.vpc = ec2.Vpc(self, 'MyVpc',

                           # 'IpAddresses' configures the IP range and size of the entire VPC.
                           # The IP space will be divided based on configuration for the subnets.
                           ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),

                           # 'maxAzs' configures the maximum number of availability zones to use.
                           # If you want to specify the exact availability zones you want the VPC
                           # to use, use `availabilityZones` instead.
                           max_azs=3,


                           # 'subnetConfiguration' specifies the "subnet groups" to create.
                           # Every subnet group will have a subnet for each AZ, so this
                           # configuration will create `3 groups × 3 AZs = 9` subnets.
                           subnet_configuration=[ec2.SubnetConfiguration(
                               # 'subnetType' controls Internet access, as described above.
                               subnet_type=ec2.SubnetType.PUBLIC,

                               # 'name' is used to name this particular subnet group. You will have to
                               # use the name for subnet selection if you have more than one subnet
                               # group of the same type.
                               name="Ingress",

                               # 'cidrMask' specifies the IP addresses in the range of of individual
                               # subnets in the group. Each of the subnets in this group will contain
                               # `2^(32 address bits - 24 subnet bits) - 2 reserved addresses = 254`
                               # usable IP addresses.
                               #
                               # If 'cidrMask' is left out the available address space is evenly
                               # divided across the remaining subnet groups.
                               cidr_mask=24
                           ), ec2.SubnetConfiguration(
                               cidr_mask=24,
                               name="Application",
                               subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                           ), ec2.SubnetConfiguration(
                               cidr_mask=28,
                               name="Database",
                               subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,

                               # 'reserved' can be used to reserve IP address space. No resources will
                               # be created for this subnet, but the IP range will be kept available for
                               # future creation of this subnet, or even for future subdivision.
                               reserved=True
                           )
                           ]
                           )

        self.vpc.apply_removal_policy(removal_policy)

        # Only reject traffic and interval every minute.
        self.vpc.add_flow_log("FlowLogCloudWatch",
                              traffic_type=ec2.FlowLogTrafficType.REJECT,
                              # max_aggregation_interval=FlowLogMaxAggregationInterval.ONE_MINUTE
                              )

        CfnOutput(self, 'VpcId',
                  description='Identifier for this VPC.',
                  value=self.vpc.vpc_id,
                  )

        CfnOutput(self, 'Vpc',
                  description='Arn of this VPC.',
                  value=self.vpc.vpc_arn,
                  )

        CfnOutput(self, 'PrivateSubnets',
                  description='List of private subnets in this VPC.',
                  value=str([s.subnet_id for s in self.vpc.private_subnets]),
                  )

        CfnOutput(self, 'IsolatedSubnets',
                  description='List of isolated subnets in this VPC.',
                  value=str([s.subnet_id for s in self.vpc.isolated_subnets]),
                  )

        CfnOutput(self, 'PublicSubnets',
                  description='List of public subnets in this VPC.',
                  value=str([s.subnet_id for s in self.vpc.public_subnets]),
                  )

        CfnOutput(self, 'AvailabilityZones',
                  description='AZs for this VPC.',
                  value=str(self.vpc.availability_zones),
                  )

        # port = 3100
        # my_security_group = ec2.SecurityGroup(self, "SecurityGroup",
        #                                       vpc=self.vpc,
        #                                       description="Allow internet access to port {}".format(port),
        #                                       allow_all_outbound=False
        #                                       )
        # my_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(port),
        #                                    "allow access from the world to port {}".format(port))
