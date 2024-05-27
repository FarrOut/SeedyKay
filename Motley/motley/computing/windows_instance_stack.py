from aws_cdk import (
    # Duration,
    CfnCondition,
    Fn,
    NestedStack,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sns as sns,
    CfnOutput,
    CfnParameter,
)
from constructs import Construct


class WindowsInstanceStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc,
        whitelisted_peer: ec2.IPeer,
        key_name: str,
        bucket: s3.IBucket = None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        toggle_param = CfnParameter(
            self,
            "ToggleParam",
            type="String",
            default="true",
        )
        is_enabled = CfnCondition(self, "IsEnabled",
                                  expression=Fn.condition_equals("true", toggle_param))

        topic = sns.Topic(self, "OffTopic")
        cfn_topic = topic.node.default_child
        cfn_topic.cfn_options.condition = is_enabled

        user_data = ec2.UserData.for_windows()
        user_data.add_commands(
            f'$topic={Fn.condition_if(is_enabled.logical_id, topic.topic_name, "false").to_string()}',
            # f'if [[ $topic != "false" ]]',
        )

        #  TODO testing DELETE!!!!!
        # #######################################################

        self.instance: ec2.Instance = None

        outer_perimeter_security_group = ec2.SecurityGroup(
            self,
            "SecurityGroup",
            vpc=vpc,
            description="Allow ssh access to ec2 instances",
            allow_all_outbound=True,
        )

        outer_perimeter_security_group.add_ingress_rule(
            whitelisted_peer,
            ec2.Port.tcp(22),
            "allow ssh access from trusted whitelist",
        )
        outer_perimeter_security_group.add_ingress_rule(
            whitelisted_peer,
            ec2.Port.udp_range(60000, 61000),
            "allow mosh access from trusted whitelist",
        )
        outer_perimeter_security_group.add_ingress_rule(
            whitelisted_peer,
            ec2.Port.tcp(3389),
            "allow RDP access from trusted whitelist",
        )
        outer_perimeter_security_group.add_ingress_rule(
            whitelisted_peer,
            ec2.Port.tcp(5985),
            "allow WinRM HTTP access from trusted whitelist",
        )
        outer_perimeter_security_group.add_ingress_rule(
            whitelisted_peer,
            ec2.Port.tcp(5986),
            "allow WinRM HTTPS access from trusted whitelist",
        )

        CfnOutput(
            self,
            "OuterPerimeterSecurityGroup",
            description="SecurityGroup acting as first-line of defence from the outside world.",
            value=outer_perimeter_security_group.security_group_id,
        )

        working_dir = "~/"
        instance_identifier = None
        handle = ec2.InitServiceRestartHandle()

        init_config_sets = ec2.CloudFormationInit.from_config_sets(
            config_sets={
                # Applies the configs below in this order
                "default": ["cfn-hup"],
                # "connectivity": ['ssh'],
            },
            configs={
                "cfn-hup": ec2.InitConfig(
                    [
                        ec2.InitFile.from_string(
                            "c:\\cfn\\cfn-hup.conf",
                            "[main]{}".format("\n")
                            + "stack={}{}".format(self.stack_name, "\n")
                            + "region={}{}".format(self.region, "\n"),
                        ),
                        ec2.InitFile.from_string(
                            "c:\\cfn\\hook.bat",
                            "echo hello > c:\\cfn\\hello.txt{}".format("\n")
                            + "cfn-init.exe -v -c default -s {} -r {} --region {} {}".format(
                                self.stack_id, "XXXXXXXXXX", self.region, "\n"
                            ),
                        ),
                        ec2.InitFile.from_string(
                            "c:\\cfn\\hooks.d\\cfn-auto-reloader.conf",
                            "[cfn-auto-reloader-hook]{}".format("\n")
                            + "triggers={}{}".format("post.update", "\n")
                            + "path=Resources.{}.Metadata.AWS::CloudFormation::Init{}".format(
                                "XXXXXXXXXX", "\n"
                            )
                            + "actions=c:\\cfn\\hook.bat {}".format("\n"),
                        ),
                        ec2.InitService.enable(
                            "cfn-hup",
                            enabled=True,
                            ensure_running=True,
                        ),
                    ]
                ),
                # 'ssh': ec2.InitConfig([
                #     ec2.InitCommand.shell_command("Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0",
                #                                   service_restart_handles=[handle]),
                #
                #     ec2.InitService.enable("sshd",
                #                            enabled=True,
                #                            ensure_running=True,
                #                            service_restart_handle=handle,
                #                            )
                # ])
            },
        )

        self.instance = ec2.Instance(
            self,
            "Instance",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM
            ),
            key_name=key_name,
            machine_image=ec2.MachineImage.latest_windows(
                ec2.WindowsVersion.WINDOWS_SERVER_2022_ENGLISH_FULL_BASE
            ),
            security_group=outer_perimeter_security_group,
            ssm_session_permissions=True,
            user_data=user_data,
            init=init_config_sets,
            init_options=ec2.ApplyCloudFormationInitOptions(
                config_sets=["default"],
                ignore_failures=True,
                print_log=True,
            ),
            user_data_causes_replacement=True,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        if bucket is not None:
            role = self.instance.role
            bucket.grant_read_write(role)
            bucket.grant_read_write(iam.AccountPrincipal(self.account))

        # Bootstrapping.get_windows_init(instance=instance, instance_role=instance.role, os_type=instance.os_type,
        #                                user_data=instance.user_data),
        # instance.applyCloudFormationInit()

        # user = 'windoze'
        # ssh_command = 'ssh' + ' -v' + ' -i ' + key_name + '.pem ' + user + '@' + instance.instance_public_dns_name
        # CfnOutput(self, 'InstanceSSHcommand',
        #           value=ssh_command,
        #           description='Command to SSH into instance.',
        #           )


class Producer:
    def produce(self, context):
        return self.instance
