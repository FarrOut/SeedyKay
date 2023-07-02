from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    aws_eks as eks, CfnOutput,
)
from aws_cdk.lambda_layer_kubectl import KubectlLayer
from constructs import Construct


class EksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.cluster = eks.Cluster(self, "HelloEKS",
                                   version=eks.KubernetesVersion.of('1.27'),
                                   kubectl_layer=KubectlLayer(self, "kubectl"),
                                   vpc=vpc,
                                   vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)],

                                   # default_capacity=3,
                                   # default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.M5,
                                   #                                               ec2.InstanceSize.SMALL)
                                   )

        CfnOutput(self, 'ClusterArn',
                  value=self.cluster.cluster_arn,
                  description='The AWS generated ARN for the Cluster resource.'
                  )
        CfnOutput(self, 'ClusterName',
                  value=self.cluster.cluster_name,
                  description='The Name of the created EKS Cluster.'
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

        eks.KubernetesManifest(self, "hello-kub",
                               cluster=self.cluster,
                               manifest=[namespace]
                               )
