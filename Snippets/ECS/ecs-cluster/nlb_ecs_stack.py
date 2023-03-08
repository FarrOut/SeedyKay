from aws_cdk import (core as cdk,
                     aws_ecs as ecs,
                     aws_ecs_patterns as ecs_patterns,
                     aws_ec2 as ec2,
                     aws_autoscaling as autoscaling,
                     )

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class NlbEcsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a cluster
        vpc = ec2.Vpc(
            self, "MyVpc",
            max_azs=2
        )

        cluster = ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )
        cluster.add_capacity("DefaultAutoScalingGroup",
                             instance_type=ec2.InstanceType.of(
                                 ec2.InstanceClass.STANDARD5,
                                 ec2.InstanceSize.MICRO))

        load_balanced_ecs_service = ecs_patterns.NetworkLoadBalancedEc2Service(self, "Service",
                                                                               cluster=cluster,
                                                                               memory_limit_mib=1024,
                                                                               task_image_options=dict(
                                                                                   image=ecs.ContainerImage.from_registry(
                                                                                       "tomcat"),
                                                                                   container_port=8080,
                                                                                   container_name='Tomcat'
                                                                               ),
                                                                               desired_count=2
                                                                               )

        cdk.CfnOutput(self, 'LoadbalancerDnsOutput',
                      value=load_balanced_ecs_service.load_balancer.load_balancer_dns_name,
                      description='Loadbalancer DNS name.'
                      )
