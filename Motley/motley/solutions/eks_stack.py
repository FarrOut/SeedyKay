import jsii
from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    CfnOutput, RemovalPolicy, Tags, Aspects, IAspect,
)
from aws_cdk.aws_eks import EndpointAccess, KubernetesVersion, Nodegroup
from aws_cdk.aws_iam import Role, ManagedPolicy, ServicePrincipal
from constructs import Construct

from motley.components.networking.vpc_stack import VpcNestedStack
from motley.components.orchestration.eks import Eks
from motley.components.orchestration.mini_eks import MiniEks


class EksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 eks_version: str, vpc: ec2.Vpc = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if vpc is None:
            net = VpcNestedStack(self, "VpcStack", removal_policy=removal_policy)
            vpc = net.vpc

        control_plane_role = Role(self, "ControlPlaneRole",
                                  assumed_by=ServicePrincipal("eks.amazonaws.com")
                                  )
        control_plane_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name("AmazonEKSClusterPolicy"))
        control_plane_role.apply_removal_policy(removal_policy)

        control_plane_sg = ec2.SecurityGroup(
            self, 'ControlPlaneSecurityGroup',
            vpc=vpc,
            allow_all_outbound=False,
            description='Security group for EKS Control Plane',
        )
        # control_plane_sg.connections.allow_from()

        tags = {
            "mytag": "v1",
            "anothertag": "Guten Tag",
            "lasertag": "bbzzzzzz"
        }

        self.cluster_stack = Eks(self, 'EksClusterStack',
                                 vpc=vpc,
                                 masters_role=None,
                                 control_plane_role=control_plane_role,
                                 control_plane_security_group=control_plane_sg,
                                 endpoint_access=EndpointAccess.PRIVATE,
                                 eks_version=KubernetesVersion.of(eks_version),
                                 tags=tags,
                                 removal_policy=removal_policy,
                                 )

        # self.cluster_stack = MiniEks(self, 'MiniEksClusterStack',
        #                              vpc=vpc,
        #                              eks_version=KubernetesVersion.of(eks_version),
        #                              tags=tags,
        #                              removal_policy=removal_policy,
        #                              )

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

        # This seems to be the source of all out problems
        for key in tags:
            Tags.of(self).add(key, tags[key],
                              exclude_resource_types=['AWS::EKS::Nodegroup', 'AWS::EC2::LaunchTemplate'], )

        # Aspects.of(self).add(TagRemoverAspect())

# @jsii.implements(IAspect)
# class TagRemoverAspect:
#     def visit(self, node):
#         if isinstance(node, Nodegroup):
#             node.node.default_child.add_deletion_override("Properties.Tags")
