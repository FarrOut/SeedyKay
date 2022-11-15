from aws_cdk import (
    Duration,
    Stack,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling, Tags,
)
from constructs import Construct


class AlbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lb = elbv2.ApplicationLoadBalancer(self, "LB",
                                           vpc=vpc,
                                           internet_facing=True
                                           )

        listener = lb.add_listener("Listener",
                                   port=80,

                                   # 'open: true' is the default, you can leave it out if you want. Set it
                                   # to 'false' and use `listener.connections` if you want to be selective
                                   # about who can access the load balancer.
                                   open=True
                                   )

        asg = autoscaling.AutoScalingGroup(self, "ASG",
                                           vpc=vpc,
                                           instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,
                                                                             ec2.InstanceSize.MICRO),
                                           machine_image=ec2.AmazonLinuxImage()
                                           )

        # Create an AutoScaling group and add it as a load balancing
        # target to the listener.
        listener.add_targets("ApplicationFleet",
                             port=8080,
                             targets=[asg]
                             )

        application_listener_rule = elbv2.ApplicationListenerRule(self, "MyApplicationListenerRule",
                                                                  listener=listener,
                                                                  priority=123,
                                                                  )

        target_group = elbv2.ApplicationTargetGroup(self, "TG1",
                                                    target_type=elbv2.TargetType.INSTANCE,
                                                    port=80,
                                                    protocol=elbv2.ApplicationProtocol.HTTP,
                                                    # health_check=health_check,
                                                    stickiness_cookie_duration=Duration.minutes(5),
                                                    vpc=vpc
                                                    )
        target_group.add_target(asg)

        target_group.configure_health_check(
            protocol=elbv2.Protocol.HTTP,
        )

        listener.add_target_groups('TargetGroups', target_groups=[target_group])
