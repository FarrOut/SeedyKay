from aws_cdk import (
    # Duration,
    NestedStack, aws_ec2 as ec2,
    aws_eks as eks, CfnOutput, RemovalPolicy,
)
from aws_cdk.aws_iam import Role, PolicyDocument, PolicyStatement, ServicePrincipal, ManagedPolicy
from aws_cdk.lambda_layer_kubectl import KubectlLayer
from constructs import Construct


class Eks(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, control_plane_role: Role,
                 version: eks.KubernetesVersion,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.cluster = eks.Cluster(self, "HelloEKS",
                                   version=version,
                                   kubectl_layer=KubectlLayer(self, "kubectl"),
                                   vpc=vpc,
                                   # vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)],
                                   # default_capacity=3,
                                   # default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.M5,
                                   #                                               ec2.InstanceSize.SMALL)
                                   role=control_plane_role,
                                   output_cluster_name=True,
                                   # output_kubeconfig=True,
                                   # output_cluster_name_as_id=True,
                                   # output_kubectl_lambda_role=True,
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

        if self.cluster.kubectl_lambda_role is not None:
            CfnOutput(self, 'KubectlLambdaRole', value=self.cluster.kubectl_lambda_role.role_arn)

        self.provider = self.cluster.stack.node.try_find_child('@aws-cdk--aws-eks.KubectlProvider')

        namespace = {
            "apiVersion": 'v1',
            "kind": 'Namespace',
            "metadata": {
                "name": 'temp-namespace',
                "labels": {
                    'test-label': 'test-value'
                }
            }
        }

        # eks.KubernetesManifest(self, "hello-kub",
        #                        cluster=self.cluster,
        #                        manifest=[namespace]
        #                        )

        ipv6_management = PolicyDocument(
            statements=[PolicyStatement(
                resources=["arn:aws:ec2:*:*:network-interface/*"],
                actions=["ec2:AssignIpv6Addresses", "ec2:UnassignIpv6Addresses"
                         ]
            )]
        )
        self.node_group_role = Role(self, "eksClusterNodeGroupRole",
                                    # role_name="eksClusterNodeGroupRole",
                                    assumed_by=ServicePrincipal("ec2.amazonaws.com"),
                                    managed_policies=[
                                        ManagedPolicy.from_aws_managed_policy_name(
                                            "AmazonEKSWorkerNodePolicy"),
                                        ManagedPolicy.from_aws_managed_policy_name(
                                            "AmazonEC2ContainerRegistryReadOnly"),
                                        ManagedPolicy.from_aws_managed_policy_name(
                                            "AmazonEKS_CNI_Policy")
                                    ],
                                    inline_policies={
                                        "ipv6_management": ipv6_management
                                    },
                                    )
        self.node_group_role.apply_removal_policy(removal_policy)
