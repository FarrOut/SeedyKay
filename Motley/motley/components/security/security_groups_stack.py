from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2, RemovalPolicy, )
from constructs import Construct


class SecurityGroupsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                              vpc=vpc,
                                              description="Testing",
                                              allow_all_outbound=True
                                              )
        my_security_group.apply_removal_policy(RemovalPolicy.DESTROY)

        my_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Test 1")
        my_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Test 2")
