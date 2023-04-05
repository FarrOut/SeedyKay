from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elb_targets,
    aws_autoscaling as autoscaling, CfnOutput, NestedStack, RemovalPolicy, Fn, Tags,
)
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy, CfnInstanceProfile
from constructs import Construct


class AutoScalingConfigStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, launch_config_name: str, vpc: ec2.Vpc,
                 whitelisted_peer: ec2.Peer, key_name: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        outer_perimeter_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                                           vpc=vpc,
                                                           description="Allow ssh access to ec2 instances",
                                                           allow_all_outbound=True,
                                                           )
        Tags.of(outer_perimeter_security_group).add('Name', 'AsgOuterPerimeter')
        outer_perimeter_security_group.add_ingress_rule(whitelisted_peer, ec2.Port.tcp(22),
                                                        "allow ssh access from the world")

        ami = ec2.MachineImage.latest_amazon_linux().get_image(self).image_id
        instance_type = ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL, )

        # Creates a userdata object for Linux hosts
        userdata = ec2.UserData.for_linux()

        # The code that defines your stack goes here
        # userdata_file = open("./scripts/userdata.sh", "rb").read()

        # Adds one or more commands to the userdata object.
        # userdata.add_commands(str(userdata_file, 'utf-8'))

        userdata.add_commands('#!/bin/bash -xe')
        userdata.add_commands('yum update -y')
        userdata.add_commands('yum install -y aws-cfn-bootstrap')
        userdata.add_commands('yum install -y java-1.8.0-openjdk')
        userdata.add_commands('yum install -y unzip')
        userdata.add_commands(
            "/opt/aws/bin/cfn-init -v --stack " + self.stack_name + " --resource " + launch_config_name +
            " --configsets install --region " + self.region)

        working_dir = '/home/ubuntu/cfn-init/'

        role = Role(self, "MyInstanceRole",
                    assumed_by=ServicePrincipal("ec2.amazonaws.com")
                    )
        # role.grant_pass_role(ServicePrincipal("ec2.amazonaws.com"))

        # role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AWSCloudFormationFullAccess"))
        role.apply_removal_policy(RemovalPolicy.DESTROY)

        instance_profile = CfnInstanceProfile(self, "MyCfnInstanceProfile",
                                              roles=[role.role_name],
                                              path="/"
                                              )

        self.launch_config = autoscaling.CfnLaunchConfiguration(self, "MyCfnLaunchConfiguration",
                                                                launch_configuration_name=launch_config_name,

                                                                image_id=ami,
                                                                ebs_optimized=True,
                                                                key_name=key_name,
                                                                instance_type=instance_type.to_string(),
                                                                iam_instance_profile=instance_profile.ref,
                                                                user_data=Fn.base64(userdata.render()),
                                                                security_groups=[
                                                                    outer_perimeter_security_group.security_group_id],
                                                                )
        self.launch_config.apply_removal_policy(RemovalPolicy.DESTROY)

        self.launch_config.add_metadata('AWS::CloudFormation::Init',
                                        {
                                            'configSets': {
                                                'install': ['nexus']
                                            },
                                            'nexus': {
                                                'commands': {
                                                    '01_DownloadNexus': {
                                                        'cwd': '/tmp',
                                                        "command": "wget https://download.sonatype.com/nexus/3/nexus-3.38"
                                                                   ".0-01-unix.tar.gz"
                                                    }
                                                }
                                            }
                                        }
                                        )

        CfnOutput(self, 'LaunchConfigurationName',
                  description='The name of the launch configuration. This name must be unique per Region per account.',
                  value=str(self.launch_config.ref),
                  )

        CfnOutput(self, 'ImageId',
                  description='The AMI ID of the image to use.',
                  value=ami,
                  )

        CfnOutput(self, 'InstanceType',
                  description='The instance type of the EC2 instance.',
                  value=instance_type.to_string(),
                  )

        self.target_group = elbv2.CfnTargetGroup(self, "MyCfnTargetGroup",
                                                 health_check_enabled=True,
                                                 health_check_path='/nexus',
                                                 health_check_protocol='HTTP',
                                                 health_check_timeout_seconds=10,
                                                 unhealthy_threshold_count=6,
                                                 healthy_threshold_count=5,
                                                 health_check_interval_seconds=120,
                                                 health_check_port='traffic-port',
                                                 matcher=elbv2.CfnTargetGroup.MatcherProperty(
                                                     http_code="302"
                                                 ),
                                                 port=8081,
                                                 protocol='HTTP',
                                                 name='nexus',
                                                 vpc_id=vpc.vpc_id,
                                                 target_type='instance',
                                                 )
