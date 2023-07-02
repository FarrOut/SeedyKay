from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2, aws_directoryservice as directoryservice, RemovalPolicy,

    CfnOutput, )
from constructs import Construct


class DirectoryStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, domain_name: str, password: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ad = directoryservice.CfnMicrosoftAD(self, "MicrosoftAD",
                                               name=domain_name,
                                               password=password,
                                               # size='Small',
                                               vpc_settings=directoryservice.CfnMicrosoftAD.VpcSettingsProperty(
                                                   subnet_ids=[vpc.private_subnets[0].subnet_id,
                                                               vpc.private_subnets[1].subnet_id],
                                                   vpc_id=vpc.vpc_id,
                                               ),

                                               # the properties below are optional
                                               create_alias=False,
                                               )
        self.ad.apply_removal_policy = RemovalPolicy.DESTROY

        CfnOutput(self, 'Ref',
                  description='The Ref for this directory.',
                  value=str(self.ad.ref),
                  )

        CfnOutput(self, 'Alias',
                  description='The alias for a directory.',
                  value=str(self.ad.attr_alias),
                  )

        # CfnOutput(self, 'IpAddresses',
        #           description='The IP addresses of the DNS servers for the directory, such as [ "192.0.2.1", '
        #                       '"192.0.2.2" ] .',
        #           value=str(self.ad.attr_dns_ip_addresses),
        #           )
        CfnOutput(self, 'Name',
                  description='The fully qualified domain name for the AWS Managed Microsoft AD directory, such as '
                              'corp.example.com . This name will resolve inside your VPC only. It does not need to be '
                              'publicly resolvable.',
                  value=str(self.ad.name),
                  )
        CfnOutput(self, 'ShortName',
                  description='The NetBIOS name for your domain, such as CORP .',
                  value=str(self.ad.short_name),
                  )
