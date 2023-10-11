from aws_cdk import (
    # Duration,
    CfnCondition,
    Fn,
    NestedStack,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sns as sns,Duration,
    CfnOutput,RemovalPolicy,
    CfnParameter,
)
from constructs import Construct
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy, PolicyStatement

class SimpleInstanceNestedStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc,
        whitelisted_peer: ec2.IPeer,
        key_name: str,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        debug_mode: bool = False,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # =====================
        # SECURITY
        # =====================

        role = Role(self, "MyInstanceRole",
                    assumed_by=ServicePrincipal("ec2.amazonaws.com")
                    )
        # role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AWSCloudFormationFullAccess"))
        role.add_to_policy(PolicyStatement(
            resources=["*"],
            actions=["ssm:UpdateInstanceInformation"]
        ))
        role.apply_removal_policy(removal_policy)

        self.outer_perimeter_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                                                vpc=vpc,
                                                                description="Allow ssh access to ec2 instances",
                                                                allow_all_outbound=True,
                                                                )
        self.outer_perimeter_security_group.apply_removal_policy(removal_policy)

        self.outer_perimeter_security_group.add_ingress_rule(whitelisted_peer, ec2.Port.tcp(22),
                                                             "allow ssh access from the world")
        self.outer_perimeter_security_group.add_ingress_rule(whitelisted_peer, ec2.Port.udp_range(60000, 61000),
                                                             "allow mosh access from the world")
        self.outer_perimeter_security_group.add_egress_rule(whitelisted_peer, ec2.Port.udp_range(60000, 60001),
                                                            "allow mosh access out to the world")
        CfnOutput(self, 'OuterPerimeterSecurityGroup',
                  description='SecurityGroup acting as first-line of defence from the outside world.',
                  value=self.outer_perimeter_security_group.security_group_id,
                  )        

        # =====================
        # COMPUTING
        # =====================

        # Ubuntu
        ubuntu_bootstrapping = ec2.UserData.for_linux()

        # # https://aws.amazon.com/premiumsupport/knowledge-center/install-cloudformation-scripts/
        # # https://gist.github.com/mmasko/66d34b651642525c63cd39251e0c2a8b#gistcomment-3931793
        ubuntu_bootstrapping.add_commands(
            'sudo apt-get -y update',
            'sudo apt-get -y upgrade',
            'sudo apt-get -y install python3 python3-pip unzip',

            # Download Cloudformation Helper Scripts
            'mkdir -p /opt/aws/bin/',

            'pip3 install https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-py3-latest.tar.gz',
            'ln -s /usr/local/init/ubuntu/cfn-hup /etc/init.d/cfn-hup',
            'ln -s /usr/local/bin/cfn-signal /opt/aws/bin/'
            'ln -s /usr/local/bin/cfn-init /opt/aws/bin/'
        )

        # Look up the most recent image matching a set of AMI filters.
        # In this case, look up the Ubuntu instance AMI
        # in the 'name' field:
        ubuntu_image = ec2.LookupMachineImage(
            # Canonical, Ubuntu, 20.04 LTS, amd64 focal image build on 2021-04-30
            # ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20210430
            name="ubuntu/images/*ubuntu-*-23.04*",
            owners=["099720109477"],
            filters={'architecture': ['x86_64']},
            user_data=ubuntu_bootstrapping,
        )
        image = ubuntu_image

        working_dir = '/home/ubuntu/'
        handle = ec2.InitServiceRestartHandle()
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html
        init_ubuntu = ec2.CloudFormationInit.from_config_sets(
            config_sets={
                # Applies the configs below in this order
                "packaging": ['install_snap'],
                "logging": ['install_cw_agent'],
                "testing": [],
                "devops": ['docker'],
                "sysadmin": ['awscli', "aws-sam-cli", "cfn-cli"],
                'connectivity': ['install_mosh'],
            },
            configs={
                'docker': ec2.InitConfig([

                    # Install Docker using the repository
                    # https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
                    ec2.InitCommand.shell_command(
                        'apt update && apt install -y ca-certificates curl gnupg lsb-release && ' +
                        'mkdir -p /etc/apt/keyrings && ' + 'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | '
                                                           'sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg && ' +
                        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] '
                        'https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee '
                        '/etc/apt/sources.list.d/docker.list > /dev/null && ' + ' apt update && ' +
                        'apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin',
                        cwd=working_dir,
                    ),

                ]),

                'awscli': ec2.InitConfig([
                    # https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
                    ec2.InitFile.from_url(
                        file_name=working_dir + 'awscliv2.zip',
                        url="https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip",
                    ),
                    ec2.InitPackage.apt(
                        package_name='unzip',
                    ),
                    ec2.InitCommand.shell_command(
                        'unzip awscliv2.zip',
                        cwd=working_dir,
                    ),
                    ec2.InitCommand.shell_command(
                        "sudo ./aws/install",
                        cwd=working_dir,
                    ),
                ]),
                'aws-sam-cli': ec2.InitConfig([
                    # Download installer package
                    # https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html#serverless-sam-cli-install-linux-sam-cli
                    ec2.InitFile.from_url(
                        file_name=working_dir + 'aws-sam-cli-linux-x86_64.zip',
                        url="https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip",
                    ),

                    # Install unzip
                    ec2.InitPackage.apt(
                        package_name='unzip',
                    ),

                    #  Extract
                    ec2.InitCommand.shell_command(
                        'unzip aws-sam-cli-linux-x86_64.zip -d sam-installation/',
                        cwd=working_dir,
                    ),

                    #  Install
                    ec2.InitCommand.shell_command(
                        "sudo ./sam-installation/install",
                        cwd=working_dir,
                    ),

                    #  Check version
                    ec2.InitCommand.shell_command(
                        "sam --version",
                        cwd=working_dir,
                    ),
                ]),
                'cfn-cli': ec2.InitConfig([
                    # Pin dependencies' versions to workaround conflicts
                    #
                    # https://stackoverflow.com/a/73199422
                    # https://github.com/aws-cloudformation/cloudformation-cli/issues/864
                    # https://github.com/aws-cloudformation/cloudformation-cli/issues/899
                    ec2.InitCommand.shell_command(
                        "pip install --upgrade requests urllib3",
                        cwd=working_dir,
                    ),
                    ec2.InitCommand.shell_command(
                        "pip install markupsafe==2.0.1 pyyaml==5.4.1",
                        cwd=working_dir,
                    ),
                    ec2.InitCommand.shell_command(
                        "pip install werkzeug==2.1.2 --no-deps",
                        cwd=working_dir,
                    ),

                    #  Install
                    # https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/what-is-cloudformation-cli.html#resource-type-setup
                    ec2.InitCommand.shell_command(
                        "pip install cloudformation-cli cloudformation-cli-java-plugin cloudformation-cli-go-plugin "
                        "cloudformation-cli-python-plugin cloudformation-cli-typescript-plugin",
                        cwd=working_dir,
                    ),
                ]),
                'install_snap': ec2.InitConfig([
                    ec2.InitPackage.apt(
                        package_name='snap',
                    ),
                ]),
                'install_mosh': ec2.InitConfig([
                    ec2.InitPackage.apt(
                        package_name='mosh',
                    ),
                    ec2.InitCommand.shell_command(
                        shell_command="sudo ufw allow 60000:61000/udp",
                        cwd=working_dir),
                ]),

                'install_cw_agent': ec2.InitConfig([

                    # Manually create or edit the CloudWatch agent configuration file
                    # https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html

                    # Installing and running the CloudWatch agent on your servers
                    # https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-commandline-fleet.html

                    ec2.InitFile.from_url(
                        file_name=working_dir + '/amazon-cloudwatch-agent.deb',
                        url='https://s3.amazonaws.com/amazoncloudwatch-agent/debian/amd64/latest/amazon-cloudwatch'
                            '-agent.deb'),
                    ec2.InitCommand.shell_command(
                        shell_command='dpkg -i -E ./amazon-cloudwatch-agent.deb',
                        cwd=working_dir)

                    # TODO Design config file and start CloudWatch agent service
                    # Installing the CloudWatch agent on new instances using AWS CloudFormation
                    # https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent-New-Instances-CloudFormation.html
                ])
            }
        )

        init = init_ubuntu
        instance = ec2.Instance(self, "Instance",
                                vpc=vpc,
                                instance_type=ec2.InstanceType.of(
                                    ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.LARGE),
                                machine_image=image,
                                key_name=key_name,
                                security_group=self.outer_perimeter_security_group,
                                role=role,
                                init=init,
                                user_data_causes_replacement=True,

                                # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/ApplyCloudFormationInitOptions.html
                                init_options=ec2.ApplyCloudFormationInitOptions(
                                    # Optional, which configsets to activate (['default'] by default)
                                    config_sets=["logging"],

                                    # Don’t fail the instance creation when cfn-init fails. You can use this to
                                    # prevent CloudFormation from rolling back when instances fail to start up,
                                    # to help in debugging. Default: false
                                    ignore_failures=debug_mode,

                                    # Force instance replacement by embedding a config fingerprint. If true (the default), a hash of the config will be embedded into the UserData, so that if the config changes, the UserData changes.
                                    embed_fingerprint=True,

                                    # Optional, how long the installation is expected to take (5 minutes by default)
                                    timeout=Duration.minutes(5),

                                    # Optional, whether to include the --url argument when running cfn-init and cfn-signal commands (false by default)
                                    include_url=False,

                                    # Optional, whether to include the --role argument when running cfn-init and cfn-signal commands (false by default)
                                    include_role=False
                                ),
                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                )

        self.instance_public_name = instance.instance_public_dns_name
        CfnOutput(self, 'InstancePublicDNSname',
                  value=self.instance_public_name,
                  description='Publicly-routable DNS name for this instance.',
                  )     

        self.instance_id = instance.instance_id                           