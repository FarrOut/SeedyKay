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

        cluster = eks.Cluster(self, "HelloEKS",
                              version=eks.KubernetesVersion.of('1.27'),
                              kubectl_layer=KubectlLayer(self, "kubectl"),
                              vpc=vpc,
                              vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)],

                              # default_capacity=3,
                              # default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.M5,
                              #                                               ec2.InstanceSize.SMALL)
                              )

        # cluster.add_nodegroup_capacity("extra-ng-spot",
        #                                instance_types=[
        #                                    ec2.InstanceType("c5.large"),
        #                                    ec2.InstanceType("c5a.large"),
        #                                    ec2.InstanceType("c5d.large")
        #                                ],
        #                                min_size=3,
        #                                capacity_type=eks.CapacityType.SPOT
        #                                )

        app_label = {"app": "hello-kubernetes"}
        deployment = {
            "api_version": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "hello-kubernetes"},
            "spec": {
                "replicas": 3,
                "selector": {"match_labels": app_label},
                "template": {
                    "metadata": {"labels": app_label},
                    "spec": {
                        "containers": [{
                            "name": "hello-kubernetes",
                            "image": "paulbouwer/hello-kubernetes:1.5",
                            "ports": [{"container_port": 8080}]
                        }
                        ]
                    }
                }
            }
        }
        service = {
            "api_version": "v1",
            "kind": "Service",
            "metadata": {"name": "hello-kubernetes"},
            "spec": {
                "type": "LoadBalancer",
                "ports": [{"port": 80, "target_port": 8080}],
                "selector": app_label
            }
        }

        # option 1: use a construct
        eks.KubernetesManifest(self, "hello-kub",
                               cluster=cluster,
                               manifest=[deployment, service]
                               )

        # # apply a kubernetes manifest to the cluster
        # cluster.add_manifest("mypod", {
        #     "api_version": "v1",
        #     "kind": "Pod",
        #     "metadata": {"name": "mypod"},
        #     "spec": {
        #         "containers": [{
        #             "name": "hello",
        #             "image": "paulbouwer/hello-kubernetes:1.5",
        #             "ports": [{"container_port": 8080}]
        #         }
        #         ]
        #     }
        # })

        CfnOutput(self, 'ClusterArn',
                  value=cluster.cluster_arn,
                  description='The AWS generated ARN for the Cluster resource.'
                  )
        CfnOutput(self, 'ClusterName',
                  value=cluster.cluster_name,
                  description='The Name of the created EKS Cluster.'
                  )
        #
        # CfnOutput(self, 'DbInstanceEndpointAddress',
        #           value=instance.db_instance_endpoint_address,
        #           description='The instance endpoint address.'
        #           )
        # CfnOutput(self, 'DbInstanceEndpointPort',
        #           value=instance.db_instance_endpoint_port,
        #           description='The instance endpoint port.'
        #           )
