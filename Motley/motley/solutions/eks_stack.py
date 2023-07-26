from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    CfnOutput, RemovalPolicy,
)
from aws_cdk.aws_eks import KubernetesVersion
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy
from constructs import Construct

from motley.components.orchestration.eks import Eks


class EksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc,
                 eks_version: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        control_plane_role = Role(self, "ControlPlaneRole",
                                  assumed_by=ServicePrincipal("eks.amazonaws.com")
                                  )
        control_plane_role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AmazonEKSClusterPolicy"))
        control_plane_role.apply_removal_policy(removal_policy)

        self.cluster_stack = Eks(self, 'EksClusterStack',
                                 vpc=vpc,
                                 control_plane_role=control_plane_role,
                                 version=KubernetesVersion.of(eks_version),
                                 )

        CfnOutput(self, 'ClusterArn',
                  value=self.cluster_stack.cluster.cluster_arn,
                  description='The AWS generated ARN for the Cluster resource.'
                  )
        CfnOutput(self, 'ClusterName',
                  value=self.cluster_stack.cluster.cluster_name,
                  description='The Name of the created EKS Cluster.'
                  )

        # self.asg = self.cluster_stack.cluster.add_auto_scaling_group_capacity(
        #     'EksClusterASG',
        #     desired_capacity=1,
        #     min_capacity=1,
        #     instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
        #     machine_image_type=MachineImageType.AMAZON_LINUX_2,
        #     update_policy=UpdatePolicy.rolling_update(
        #         max_batch_size=3,
        #         min_instances_in_service=1,
        #     ),
        #     termination_policies=[TerminationPolicy.ALLOCATION_STRATEGY, TerminationPolicy.OLDEST_INSTANCE,
        #                           TerminationPolicy.DEFAULT],
        # )
        # CfnOutput(self, 'ClusterAsgName',
        #           value=self.asg.auto_scaling_group_name,
        #           description='The Name of the created EKS Cluster ASG.'
        #           )
        # CfnOutput(self, 'ClusterAsgArn', value=self.asg.auto_scaling_group_arn,
        #           description='The Arn  of the created EKS Cluster ASG.')
        #
        # Tags.of(self.asg).add("Label", "Added at cluster-level")

        eks_optimized_image = ec2.LookupMachineImage(
            name=f"amazon-eks-node-{eks_version}-*",
            owners=["amazon"],
            filters={'architecture': ['x86_64'], 'state': ['available']},
            # user_data=ubuntu_bootstrapping,
        )
        lt = ec2.LaunchTemplate(self, "LaunchTemplate",
                                machine_image=eks_optimized_image,
                                )

        node_group = self.cluster_stack.cluster.add_nodegroup_capacity(
            'EksClusterNodeGroup',
            min_size=1,  # Default: 1
            desired_size=2,  # Default: 2
            # launch_template_spec=LaunchTemplateSpec(
            #     id=lt.launch_template_id,
            #     version=lt.latest_version_number
            # ),
            node_role=self.cluster_stack.node_group_role,
            tags={
                'Name': 'EKS Cluster Node Group',
                'Label': 'Added at cluster-level'
            },
        )

        CfnOutput(self, 'NodeGroupInstanceProfileRole',
                  value=node_group.role.role_arn,
                  description='IAM role of the instance profile for the nodegroup.'
                  )
