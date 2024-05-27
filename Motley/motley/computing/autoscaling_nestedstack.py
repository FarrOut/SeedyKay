from aws_cdk import (
    # Duration,
    NestedStack,
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elb_targets,
    aws_autoscaling as autoscaling, CfnOutput, RemovalPolicy, Fn, Tags, )
from constructs import Construct

from motley.computing.autoscaling_config_stack import AutoScalingConfigStack


class AutoScalingNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, whitelisted_peer: ec2.Peer, key_name: str,
                 removal_policy: RemovalPolicy,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO Create LaunchTemplate

        asg_config_stack = AutoScalingConfigStack(self, "AutoScalingConfigStack",
                                                  launch_config_name="Apollo12",
                                                  vpc=vpc,
                                                  key_name=key_name,
                                                  whitelisted_peer=whitelisted_peer,
                                                  )

        self.asg = autoscaling.AutoScalingGroup(self, "ASG",
                                                vpc=vpc,
                                                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,
                                                                                  ec2.InstanceSize.MICRO),

                                                # The latest Amazon Linux image of a particular generation
                                                machine_image=ec2.MachineImage.latest_amazon_linux2(),
                                                )
        self.asg.apply_removal_policy(removal_policy)

        CfnOutput(self, 'AsgName',
                  description='The name of the Auto Scaling group. This name must be unique per Region per account.',
                  value=str(self.asg.auto_scaling_group_name),
                  )
