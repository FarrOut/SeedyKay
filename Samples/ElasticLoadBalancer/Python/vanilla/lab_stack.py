from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as autoscaling,
)
from constructs import Construct


class LabStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC")

        asg = autoscaling.AutoScalingGroup(self, "ASG",
                                           vpc=vpc,
                                           instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,
                                                                             ec2.InstanceSize.MICRO),
                                           machine_image=ec2.AmazonLinuxImage()
                                           )

        lb = elbv2.ApplicationLoadBalancer(self, "LB",
                                           vpc=vpc,
                                           internet_facing=False,
                                           )

        listener = lb.add_listener("listener", port=80)

        # health_check = elbv2.HealthCheck(
        #     interval=Duration.seconds(11),
        #     path='/',
        #     port='80',
        #     protocol=elbv2.Protocol.HTTP,
        #     timeout=Duration.seconds(10),
        #     healthy_http_codes="200,202",
        # )

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
