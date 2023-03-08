from aws_cdk import (core as cdk,
                     aws_route53 as r53,
                     aws_route53_targets as r53targets,
                     aws_ec2 as ec2,
                     aws_elasticloadbalancingv2 as elb,
                     )

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class DemoStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_ = ec2.Vpc(self, 'myVPC')

        elb_ = elb.ApplicationLoadBalancer(self, 'myBalancer',
                                           vpc=vpc_,
                                           )

        zone_ = r53.HostedZone(self, 'DropZone',
                               zone_name='alb.example.com')

        target_ = r53.RecordTarget.from_alias(r53targets.LoadBalancerTarget(elb_))

        record_ = r53.ARecord(self, 'GoldRecord',
                              target=target_,
                              zone=zone_,
                              )
