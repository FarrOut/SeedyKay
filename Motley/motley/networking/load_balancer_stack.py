import logging

from aws_cdk import (
    # Duration,
    NestedStack,
    RemovalPolicy,
    Stack,aws_elasticloadbalancingv2 as elbv2,
    aws_ec2 as ec2, CfnOutput, )
from constructs import Construct


class LoadBalancerStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, removal_policy: RemovalPolicy, internet_facing: bool=True,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lb = elbv2.ApplicationLoadBalancer(self, "LB",
            vpc=vpc,
            internet_facing=internet_facing,            
        )        
        self.lb.apply_removal_policy(removal_policy)

        # Outputs
        CfnOutput(self, "LoadBalancerName", value=self.lb.load_balancer_name, description='The name of this load balancer.')
        CfnOutput(self, "LoadBalancerFullName", value=self.lb.load_balancer_full_name, description='The full name of this load balancer.')
        CfnOutput(self, "LoadBalancerDnsName", value=self.lb.load_balancer_dns_name, description='The DNS name of this load balancer.')
        CfnOutput(self, "LoadBalancerCanonicalHostedZoneId", value=self.lb.load_balancer_canonical_hosted_zone_id, description='The canonical hosted zone ID of this load balancer.')
        CfnOutput(self, "LoadBalancerArn", value=self.lb.load_balancer_arn, description='The ARN of this load balancer.')                                

        # # Add a listener and open up the load balancer's security group
        # # to the world.
        # listener = self.lb.add_listener("Listener",
        #     port=80,

        #     # 'open: true' is the default, you can leave it out if you want. Set it
        #     # to 'false' and use `listener.connections` if you want to be selective
        #     # about who can access the load balancer.
        #     open=True
        # )

        # # Create an AutoScaling group and add it as a load balancing
        # # target to the listener.
        # listener.add_targets("ApplicationFleet",
        #     port=8080,
        #     targets=[asg]
        # )        