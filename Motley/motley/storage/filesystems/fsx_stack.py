from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2, aws_fsx as fsx, CfnOutput, )
from aws_cdk.aws_directoryservice import CfnMicrosoftAD
from constructs import Construct


class FSxStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, active_directory: CfnMicrosoftAD,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        CfnOutput(self, 'Subnets',
                  description='List of private subnets in this VPC.',
                  value=str([s.subnet_id for s in vpc.private_subnets]),
                  )

        # subnets = vpc.select_subnets(subnet_type= ec2.SubnetType.PRIVATE).subnet_ids

        fs = fsx.CfnFileSystem(self, "FSxForWindowsFileSystem",
                               file_system_type='WINDOWS',
                               storage_capacity=32,
                               # subnet_ids=[str(s.subnet_id) for s in vpc.private_subnets],
                               subnet_ids=[vpc.private_subnets[0].subnet_id],
                               windows_configuration=fsx.CfnFileSystem.WindowsConfigurationProperty(
                                   active_directory_id=active_directory.ref,
                                   throughput_capacity=8,
                                   weekly_maintenance_start_time='1:03:00',
                                   automatic_backup_retention_days=7,
                                   daily_automatic_backup_start_time='02:00',
                                   copy_tags_to_backups=True,
                                   aliases=[active_directory.name],
                                   # self_managed_active_directory_configuration=
                                   # fsx.CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty(
                                   #     dns_ips=["10.0.101.211", "10.0.36.142"],
                                   #     domain_name=domain_name,
                                   #     password='(@yFh&#Tu7+phYas',
                                   #     user_name="Admin"
                                   # ),
                               ))

        CfnOutput(self, 'FileSystemDnsName',
                  description='Returns the FSx for Windows file system’s DNSName.',
                  value=str(fs.attr_dns_name)
                  )
        CfnOutput(self, 'FileSystemArn',
                  description='Returns the Amazon Resource Name (ARN) for the Amazon FSx file system.',
                  value=str(fs.attr_resource_arn)
                  )
        CfnOutput(self, 'FileSystemType',
                  description='The type of Amazon FSx file system, which can be LUSTRE , WINDOWS , ONTAP , or OPENZFS.',
                  value=str(fs.file_system_type)
                  )
        CfnOutput(self, 'FileSystemKmsKeyId',
                  description='The ID of the AWS Key Management Service ( AWS KMS ) key used to encrypt Amazon FSx '
                              'file system data.',
                  value=str(fs.kms_key_id)
                  )
        CfnOutput(self, 'FileSystemStorageCapacity',
                  description='Sets the storage capacity of the file system that you’re creating.',
                  value=str(fs.storage_capacity)
                  )
        CfnOutput(self, 'FileSystemStorageType',
                  description='Sets the storage type for the file system that you’re creating. Valid values are SSD '
                              'and HDD .',
                  value=str(fs.storage_type)
                  )

        security_group = ec2.SecurityGroup(self, "FSxSG",
                                           vpc=vpc,
                                           allow_all_outbound=False,
                                           allow_all_ipv6_outbound=False,
                                           )
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(445)
        )
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(135)
        )
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.udp(138)
        )
        async_connection = ec2.Connections(security_groups=[security_group])
        async_connection.allow_from_any_ipv4(port_range=ec2.Port.tcp(1024))
        async_connection.allow_to_any_ipv4(port_range=ec2.Port.tcp(65535))
        async_connection.allow_to(other=ec2.Peer.any_ipv4(), port_range=ec2.Port.tcp(65535))
        # security_group.add_ingress_rule(
        #     peer=ec2.Peer.any_ipv4(),
        #     connection=async_connection,
        # )
