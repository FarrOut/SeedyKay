from aws_cdk.aws_ec2 import SubnetType
from aws_cdk import (
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    core as cdk,
)


class DemoStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        keypair = 'xxxxx'

        # The code that defines your stack goes here
        userdata_file = open("./userdata.sh", "rb").read()

        # Creates a userdata object for Linux hosts
        userdata = ec2.UserData.for_linux()
        # Adds one or more commands to the userdata object.
        userdata.add_commands(str(userdata_file, 'utf-8'))

        vpc = ec2.Vpc(self, "TheVPC")

        offical_image = ec2.AmazonLinuxImage(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
        )
        custom_image = ec2.MachineImage.generic_linux({
                                                 "eu-west-1": "ami-0375ac97be47f1848" # RHEL_8.4-x86_64-SQL_2019_Web-2021.07.14
                                             })

        asg = autoscaling.AutoScalingGroup(
            self,
            "app-asg",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL
            ),
            machine_image=custom_image,
            key_name=keypair,
            vpc_subnets=ec2.SubnetSelection(subnet_type=SubnetType.PRIVATE),
            user_data=userdata,
        )
