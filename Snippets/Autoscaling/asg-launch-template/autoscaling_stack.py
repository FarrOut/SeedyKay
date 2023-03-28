from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
)
from constructs import Construct


class AutoscalingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        template = ec2.LaunchTemplate(self, "LaunchTemplate",
                                      machine_image=ec2.MachineImage.latest_amazon_linux(),
                                      instance_type=c,
                                      )

        asg = autoscaling.AutoScalingGroup(
            self,
            "asg",
            vpc=vpc,
            launch_template=template,
        )
