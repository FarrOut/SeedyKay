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
        self.vpc = ec2.Vpc(self, 'MyVpc')
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
