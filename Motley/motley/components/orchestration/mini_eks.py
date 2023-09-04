from aws_cdk import (
    # Duration,
    NestedStack, aws_ec2 as ec2,
    aws_eks as eks, CfnOutput, RemovalPolicy, Tags
)
from aws_cdk.aws_eks import LaunchTemplateSpec, KubernetesVersion, ClusterLoggingTypes
from aws_cdk.aws_iam import Role, PolicyDocument, PolicyStatement, ServicePrincipal, ManagedPolicy, AccountPrincipal
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer

from constructs import Construct


class MiniEks(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc,
                 eks_version: KubernetesVersion, tags: dict = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # select subnet
        cluster_subnets = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)

        self.cluster = eks.Cluster(self, "HelloEKS",
                                   version=eks_version,
                                   vpc=vpc,
                                   vpc_subnets=[cluster_subnets],
                                   default_capacity=0,
                                   # control_plane_security_group=control_plane_security_group,
                                   endpoint_access=eks.EndpointAccess.PUBLIC,
                                   output_cluster_name=True,
                                   tags=tags,
                                   )

        CfnOutput(self, 'ClusterArn',
                  value=self.cluster.cluster_arn,
                  description='The AWS generated ARN for the Cluster resource.'
                  )
        CfnOutput(self, 'ClusterName',
                  value=self.cluster.cluster_name,
                  description='The Name of the created EKS Cluster.'
                  )
        CfnOutput(self, 'ClusterRoleArn',
                  value=self.cluster.role.role_arn,
                  description='IAM role assumed by the EKS Control Plane.'
                  )

        CfnOutput(self, 'OidcProvider', value=self.cluster.open_id_connect_provider.open_id_connect_provider_arn)
        CfnOutput(self, 'SecurityGroupId', value=self.cluster.cluster_security_group_id)
        CfnOutput(self, 'KubectlRole', value=self.cluster.kubectl_role.role_arn)

        lt = ec2.LaunchTemplate(self, "LaunchTemplate",
                                launch_template_name="testcluster-lt",
                                detailed_monitoring=False,
                                )
        lt.apply_removal_policy(removal_policy)

        node_group = self.cluster.add_nodegroup_capacity(
            'EksClusterNodeGroup',
            min_size=1,  # Default: 1
            desired_size=3,  # Default: 2
            nodegroup_name="tagging-testcluster-ng",
            launch_template_spec=LaunchTemplateSpec(
                id=lt.launch_template_id,
                version=lt.latest_version_number
            ),
            ami_type=eks.NodegroupAmiType.AL2_X86_64,
            instance_types=[ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,
                                                ec2.InstanceSize.MICRO)],
            subnets=cluster_subnets,
        )
        node_group.role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'))

        CfnOutput(self, 'NodeGroupInstanceProfileRole',
                  value=node_group.role.role_arn,
                  description='IAM role of the instance profile for the nodegroup.'
                  )
