from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling, CfnOutput,
)
from constructs import Construct


class AutoScalingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ami = ec2.MachineImage.latest_amazon_linux().get_image(self).image_id
        instance_type = ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL, )

        launch_config = autoscaling.CfnLaunchConfiguration(self, "MyCfnLaunchConfiguration",
                                                           launch_configuration_name="Apollo11",

                                                           image_id=ami,
                                                           instance_type=instance_type.to_string())

        cfnAsg = autoscaling.CfnAutoScalingGroup(self, "CfnAutoScalingGroup",
                                                 min_size="0",
                                                 max_size="6",
                                                 desired_capacity="1",

                                                 launch_configuration_name=launch_config.launch_configuration_name,
                                                 availability_zones=vpc.availability_zones,
                                                 )

        CfnOutput(self, 'AsgName',
                  description='The name of the Auto Scaling group. This name must be unique per Region per account.',
                  value=str(cfnAsg.auto_scaling_group_name),
                  )

        CfnOutput(self, 'LaunchConfigurationName',
                  description='The name of the launch configuration. This name must be unique per Region per account.',
                  value=str(launch_config.launch_configuration_name),
                  )

        CfnOutput(self, 'ImageId',
                  description='The AMI ID of the image to use.',
                  value=ami,
                  )

        CfnOutput(self, 'InstanceType',
                  description='The instance type of the EC2 instance.',
                  value=instance_type.to_string(),
                  )
