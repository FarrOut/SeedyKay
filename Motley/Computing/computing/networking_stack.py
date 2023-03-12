from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2, CfnOutput, RemovalPolicy, Tags,
)
from constructs import Construct


class NetworkingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, 'MyVpc', )

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
