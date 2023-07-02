from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    aws_eks as eks, CfnOutput,
)
from constructs import Construct


class ImportedEksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, cluster: eks.Cluster,
                 kubectl_provider: eks.IKubectlProvider,
                 # lb_security_group: ec2.SecurityGroup, control_plane_security_group: ec2.SecurityGroup,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        CfnOutput(self, 'ImportedProviderRoleArn',
                  value=kubectl_provider.role_arn,
                  description='Arn of the imported Provider''s Role.'
                  )
        CfnOutput(self, 'ImportedProviderHandlerRoleArn',
                  value=kubectl_provider.handler_role.role_arn,
                  description='Arn of the imported Provider''s Handler Role.'
                  )
        CfnOutput(self, 'ImportedProviderServiceToken',
                  value=kubectl_provider.service_token,
                  description='Arn of the imported Provider''s service token.'
                  )

        imported_cluster = eks.Cluster.from_cluster_attributes(
            scope=self,
            id=f'ImportedEKSCluster',
            cluster_name=cluster.cluster_name,
            cluster_endpoint=cluster.cluster_endpoint,
            open_id_connect_provider=cluster.open_id_connect_provider,
            # kubectl_private_subnet_ids=subnet_ids,
            # kubectl_security_group_id=control_plane_security_group.security_group_id,
            kubectl_provider=kubectl_provider,
            vpc=vpc,
        )

        CfnOutput(self, 'ClusterArn',
                  value=imported_cluster.cluster_arn,
                  description='The AWS generated ARN for the Cluster resource.'
                  )
        CfnOutput(self, 'ClusterName',
                  value=imported_cluster.cluster_name,
                  description='The Name of the created EKS Cluster.'
                  )

        CfnOutput(self, 'OidcProvider', value=imported_cluster.open_id_connect_provider.open_id_connect_provider_arn)
        # CfnOutput(self, 'SecurityGroupId', value=imported_cluster.cluster_security_group_id)

        if imported_cluster.kubectl_role is not None:
            CfnOutput(self, 'KubectlRole', value=imported_cluster.kubectl_role.role_arn)

        if imported_cluster.kubectl_lambda_role is not None:
            CfnOutput(self, 'KubectlLambdaRole', value=imported_cluster.kubectl_lambda_role.role_arn)

        namespace = {
            "apiVersion": 'v1',
            "kind": 'Namespace',
            "metadata": {
                "name": 'another-namespace',
                "labels": {
                    'test-label': 'added-to-imported-EKS-cluster-yay'
                }
            }
        }
        eks.KubernetesManifest(self, "hello-kub",
                               cluster=imported_cluster,
                               manifest=[namespace]
                               )
