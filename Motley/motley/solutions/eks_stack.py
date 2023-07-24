from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    CfnOutput,
)
from aws_cdk.aws_autoscaling import TerminationPolicy, UpdatePolicy
from aws_cdk.aws_eks import MachineImageType
from constructs import Construct

from motley.components.orchestration.eks import Eks


class EksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.cluster_stack = Eks(self, 'EksClusterStack',
                                 vpc=vpc,
                                 )

        CfnOutput(self, 'ClusterArn',
                  value=self.cluster_stack.cluster.cluster_arn,
                  description='The AWS generated ARN for the Cluster resource.'
                  )
        CfnOutput(self, 'ClusterName',
                  value=self.cluster_stack.cluster.cluster_name,
                  description='The Name of the created EKS Cluster.'
                  )

        self.asg = self.cluster_stack.cluster.add_auto_scaling_group_capacity(
            'EksClusterASG',
            desired_capacity=1,
            min_capacity=1,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image_type=MachineImageType.AMAZON_LINUX_2,
            update_policy=UpdatePolicy.rolling_update(
                max_batch_size=3,
                min_instances_in_service=1,
            ),
            termination_policies=[TerminationPolicy.ALLOCATION_STRATEGY, TerminationPolicy.OLDEST_INSTANCE,
                                  TerminationPolicy.DEFAULT]
        )
        CfnOutput(self, 'ClusterAsgName',
                  value=self.asg.auto_scaling_group_name,
                  description='The Name of the created EKS Cluster ASG.'
                  )
        CfnOutput(self, 'ClusterAsgArn', value=self.asg.auto_scaling_group_arn,
                  description='The Arn  of the created EKS Cluster ASG.')
