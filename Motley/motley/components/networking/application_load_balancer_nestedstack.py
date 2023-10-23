import logging

from aws_cdk import (
    # Duration,
    NestedStack,
    RemovalPolicy, aws_codedeploy as codedeploy,
    Stack, aws_elasticloadbalancingv2 as elbv2, aws_elasticloadbalancing as elb,
    aws_ec2 as ec2, CfnOutput, )
from constructs import Construct


class LoadBalancerNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, removal_policy: RemovalPolicy, internet_facing: bool = False,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.alb = elbv2.ApplicationLoadBalancer(self, "LB",
                                                 vpc=vpc,
                                                 internet_facing=internet_facing,
                                                 deletion_protection=((removal_policy == RemovalPolicy.RETAIN) or (
                                                     removal_policy == RemovalPolicy.SNAPSHOT)),
                                                 )
        self.alb.apply_removal_policy(removal_policy)

        # Outputs
        CfnOutput(self, "LoadBalancerName", value=self.alb.load_balancer_name,
                  description='The name of this load balancer.')
        CfnOutput(self, "LoadBalancerFullName", value=self.alb.load_balancer_full_name,
                  description='The full name of this load balancer.')
        CfnOutput(self, "LoadBalancerDnsName", value=self.alb.load_balancer_dns_name,
                  description='The DNS name of this load balancer.')
        CfnOutput(self, "LoadBalancerCanonicalHostedZoneId", value=self.alb.load_balancer_canonical_hosted_zone_id,
                  description='The canonical hosted zone ID of this load balancer.')
        CfnOutput(self, "LoadBalancerArn", value=self.alb.load_balancer_arn,
                  description='The ARN of this load balancer.')

        # listener = self.alb.add_listener("Listener", port=80)
        # target_group = listener.add_targets("Fleet", port=80)

        # CfnOutput(self, "TargetGroupArn", value=target_group.target_group_arn,
        #           description='The ARN of this target group.')
        # CfnOutput(self, "TargetGroupFullName", value=target_group.target_group_full_name,
        #           description='The full name of this target group.')

        # self.lb = codedeploy.LoadBalancer.application(target_group)

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
