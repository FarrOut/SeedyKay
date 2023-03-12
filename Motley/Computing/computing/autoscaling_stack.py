from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elb_targets,
    aws_autoscaling as autoscaling, CfnOutput, RemovalPolicy, Fn, Tags, )
from constructs import Construct

from computing.autoscaling_config_stack import AutoScalingConfigStack


class AutoScalingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, whitelisted_peer: ec2.Peer, key_name: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        asg_config_stack = AutoScalingConfigStack(self, "AutoScalingConfigStack",
                                                  vpc=vpc,
                                                  key_name=key_name,
                                                  whitelisted_peer=whitelisted_peer,
                                                  )

        cfn_asg = autoscaling.CfnAutoScalingGroup(self, "CfnAutoScalingGroup",
                                                  min_size="0",
                                                  max_size="6",
                                                  desired_capacity="1",

                                                  launch_configuration_name=asg_config_stack.launch_config.ref,
                                                  target_group_arns=[
                                                      asg_config_stack.target_group.ref],
                                                  # availability_zones=vpc.availability_zones,
                                                  vpc_zone_identifier=[str(vpc.public_subnets[0].subnet_id),
                                                                       str(vpc.public_subnets[1].subnet_id)],
                                                  )

        # cfn_asg.add_dependency(config_stack)

        CfnOutput(self, 'AsgName',
                  description='The name of the Auto Scaling group. This name must be unique per Region per account.',
                  value=str(cfn_asg.auto_scaling_group_name),
                  )

        # listener = elbv2.CfnListener(self, "MyCfnListener",
        #
        #                              )
        #
        # listener_rule = elbv2.CfnListenerRule(self, "MyCfnListenerRule",
        #                                       actions=[
        #                                           elbv2.CfnListenerRule.ActionProperty(
        #                                               type='forward',
        #                                               target_group_arn=target_group.ref
        #                                           )
        #                                       ],
        #                                       conditions=[
        #                                           elbv2.CfnListenerRule.RuleConditionProperty(
        #                                               field='path-pattern',
        #                                               path_pattern_config=elbv2.CfnListenerRule.PathPatternConfigProperty(
        #                                                   values=["/nexus*"]
        #                                               )
        #                                           )
        #                                       ],
        #                                       priority='91',
        #                                       listener_arn=listener.ref
        #                                       )
