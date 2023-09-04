from aws_cdk import (
    # Duration,
    NestedStack,
    RemovalPolicy, aws_elasticloadbalancingv2 as elbv2, aws_ec2 as ec2, CfnOutput, )
from constructs import Construct


class ElbStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, removal_policy: RemovalPolicy,
                 internet_facing: bool = True, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        elb = elbv2.CfnLoadBalancer(self, "MyCfnLoadBalancer",
                                    ip_address_type="ipv4",
                                    name="NLB",
                                    scheme="internal",
                                    subnet_mappings=[elbv2.CfnLoadBalancer.SubnetMappingProperty(
                                        subnet_id=vpc.private_subnets[0].subnet_id,
                                    ), elbv2.CfnLoadBalancer.SubnetMappingProperty(
                                        subnet_id=vpc.private_subnets[1].subnet_id,
                                    )],
                                    type="network"
                                    )
        elb.apply_removal_policy(removal_policy)

        CfnOutput(self, "LoadBalancerName", value=elb.name, description='The name of this load balancer.')
        CfnOutput(self, "LoadBalancerFullName", value=elb.attr_load_balancer_full_name,
                  description='The full name of this load balancer.')
        # CfnOutput(self, "LoadBalancerId", value=elb.attr_id, description='The ID of this load balancer.')
        CfnOutput(self, "LoadBalancerDNSName", value=elb.attr_dns_name,
                  description='The DNS name of this load balancer.')
        CfnOutput(self, "LoadBalancerCanonicalHostedZoneId", value=elb.attr_canonical_hosted_zone_id,
                  description='The ID of the Amazon Route 53 hosted zone associated with the load balancer.')
