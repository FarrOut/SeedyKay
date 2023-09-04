from aws_cdk import (
    # Duration,
    NestedStack, aws_ec2 as ec2,
    aws_eks as eks, CfnOutput, RemovalPolicy, Tags
)
from aws_cdk.aws_eks import LaunchTemplateSpec, KubernetesVersion, ClusterLoggingTypes
from aws_cdk.aws_iam import Role, PolicyDocument, PolicyStatement, ServicePrincipal, ManagedPolicy, AccountPrincipal
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer

from constructs import Construct


class Eks(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, masters_role: Role, control_plane_role: Role,
                 eks_version: KubernetesVersion, control_plane_security_group: ec2.SecurityGroup,
                 endpoint_access: eks.EndpointAccess,
                 tags: dict = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        kubectl_layer = KubectlV24Layer(self, "kubectl")
        kubectl_layer.apply_removal_policy(removal_policy)

        masters_role = Role(self, 'MastersRole',
                            assumed_by=AccountPrincipal(
                                account_id=self.account))

        self.cluster = eks.Cluster(self, "HelloEKS",
                                   version=eks_version,
                                   kubectl_layer=kubectl_layer,
                                   vpc=vpc,
                                   # vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)],
                                   default_capacity=0,
                                   # default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.M5,
                                   #                                               ec2.InstanceSize.SMALL)
                                   role=control_plane_role,
                                   masters_role=masters_role,
                                   # control_plane_security_group=control_plane_security_group,
                                   endpoint_access=eks.EndpointAccess.PUBLIC,
                                   output_cluster_name=True,
                                   output_masters_role_arn=True,
                                   output_config_command=True,
                                   cluster_logging=[ClusterLoggingTypes.API,
                                                    ClusterLoggingTypes.AUTHENTICATOR,
                                                    ClusterLoggingTypes.SCHEDULER,
                                                    ClusterLoggingTypes.CONTROLLER_MANAGER,
                                                    ClusterLoggingTypes.AUDIT,
                                                    ],
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

        self.cluster.add_manifest("mypod", {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": "mypod"},
            "spec": {
                "containers": [{
                    "name": "hello",
                    "image": "paulbouwer/hello-kubernetes:1.5",
                    "ports": [{"containerPort": 8080}]
                }
                ]
            }
        })

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

        # eks_optimized_image = ec2.LookupMachineImage(
        #     name=f"amazon-eks-node-{eks_version}-*",
        #     owners=["amazon"],
        #     filters={'architecture': ['x86_64'], 'state': ['available']},
        # )

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            'MIME-Version: 1.0',
            'Content-Type: multipart/mixed; boundary="==MYBOUNDARY=="',
            '',
            '--==MYBOUNDARY==',
            'Content-Type: text/cloud-config; charset="us-ascii"',
            '',
            '#!/bin/bash',
            'set -e',
            f'/etc/eks/bootstrap.sh {self.cluster.cluster_name}',
            '',
            '--==MYBOUNDARY==',
        )
        lt = ec2.LaunchTemplate(self, "LaunchTemplate",
                                # machine_image=eks_optimized_image,
                                user_data=user_data,
                                http_endpoint=True,
                                http_protocol_ipv6=False,
                                http_put_response_hop_limit=1,
                                http_tokens=ec2.LaunchTemplateHttpTokens.REQUIRED,
                                instance_metadata_tags=True,
                                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,
                                                                  ec2.InstanceSize.MICRO),
                                )
        Tags.of(lt).add('Name', 'EKS Cluster Launch Template')
        lt.apply_removal_policy(removal_policy)

        node_group = self.cluster.add_nodegroup_capacity(
            'EksClusterNodeGroup',
            min_size=1,  # Default: 1
            desired_size=3,  # Default: 2
            launch_template_spec=LaunchTemplateSpec(
                id=lt.launch_template_id,
                version=lt.latest_version_number
            ),
            node_role=self.node_group_role,
            ami_type=eks.NodegroupAmiType.AL2_X86_64,
            tags={
                'Name': 'EKS Cluster Node Group',
                'Label': 'Updated at cluster-level'
            },
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
        )
        node_group.role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'))

        CfnOutput(self, 'NodeGroupInstanceProfileRole',
                  value=node_group.role.role_arn,
                  description='IAM role of the instance profile for the nodegroup.'
                  )
