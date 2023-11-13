from aws_cdk import (
    # Duration,
    NestedStack, aws_sagemaker as sagemaker, aws_iam as iam, aws_ec2 as ec2,
    RemovalPolicy, CfnOutput, )
from constructs import Construct

from motley.components.networking.vpc_stack import VpcNestedStack


class SageMakerDomainNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN, vpc: ec2.Vpc = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if vpc is None:
            net = VpcNestedStack(
                self, "VpcStack", removal_policy=removal_policy)
            vpc = net.vpc

        role = iam.Role(self, "ExecutionRole",
                        assumed_by=iam.ServicePrincipal(
                            "sagemaker.amazonaws.com")
                        )

        security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                           vpc=vpc,
                                           description="Testing",
                                           allow_all_outbound=True
                                           )
        security_group.apply_removal_policy(removal_policy)

        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Test 1")
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Test 2")

        domain = sagemaker.CfnDomain(self, 'Domain',
                                     app_network_access_type='VpcOnly',
                                     auth_mode='IAM',
                                     default_user_settings=sagemaker.CfnDomain.UserSettingsProperty(
                                         execution_role=role.role_arn,
                                         security_groups=[
                                             security_group.security_group_id],
                                     ),
                                     domain_name='sagemaker-domain',
                                     vpc_id=vpc.vpc_id,
                                     subnet_ids=[
                                         s.subnet_id for s in vpc.private_subnets],
                                     )

        domain.apply_removal_policy(removal_policy)

        CfnOutput(self, 'DomainArn', value=domain.attr_domain_arn,
                  description='The Amazon Resource Name (ARN) of the Domain, such as arn:aws:sagemaker:us-west-2:account-id:domain/my-domain-name .')
        CfnOutput(self, 'DomainId', value=domain.attr_domain_id,
                  description='The Domain ID.')
        CfnOutput(self, 'AppNetworkAccessType', value=domain.app_network_access_type,
                  description='Specifies the VPC used for non-EFS traffic.')
        CfnOutput(self, 'DomainUrl', value=domain.attr_url,
                  description='The URL for the Domain.')
        CfnOutput(self, 'DomainName', value=domain.domain_name,
                  description='The domain name.')
        CfnOutput(self, 'DomainVpcId', value=domain.vpc_id,
                  description='The ID of the Amazon Virtual Private Cloud (Amazon VPC) that Studio uses for communication.')
        CfnOutput(self, 'AuthMode', value=domain.auth_mode,
                  description='The mode of authentication that members use to access the Domain.')
