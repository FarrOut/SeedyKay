from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    CfnOutput, )
from constructs import Construct


class InstanceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, whitelisted_peer: ec2.Peer, key_name: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        outer_perimeter_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                                           vpc=vpc,
                                                           description="Allow ssh access to ec2 instances",
                                                           allow_all_outbound=True
                                                           )

        outer_perimeter_security_group.add_ingress_rule(whitelisted_peer, ec2.Port.tcp(22),
                                                        "allow ssh access from the world")
        outer_perimeter_security_group.add_ingress_rule(whitelisted_peer, ec2.Port.udp_range(60000, 61000),
                                                        "allow mosh access from the world")

        CfnOutput(self, 'OuterPerimeterSecurityGroup',
                  description='SecurityGroup acting as first-line of defence from the outside world.',
                  value=outer_perimeter_security_group.security_group_id,
                  )

        user_data = ec2.UserData.for_windows()

        instance = ec2.Instance(self, 'Instance',
                                vpc=vpc,
                                instance_type=ec2.InstanceType.of(
                                    ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
                                key_name=key_name,
                                machine_image=ec2.MachineImage.latest_windows(
                                    ec2.WindowsVersion.WINDOWS_SERVER_2022_ENGLISH_FULL_SQL_2019_STANDARD),
                                security_group=outer_perimeter_security_group,
                                user_data=user_data,
                                )

        user = 'windoze'
        ssh_command = 'ssh' + ' -v' + ' -i ' + key_name + '.pem ' + user + '@' + instance.instance_public_dns_name
        CfnOutput(self, 'InstanceSSHcommand',
                  value=ssh_command,
                  description='Command to SSH into instance.',
                  )
