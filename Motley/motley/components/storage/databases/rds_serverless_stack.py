from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    CfnOutput, RemovalPolicy,
)
from constructs import Construct


class RdsServerlessStack(Stack):
    def __init__(
            self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cluster = rds.DatabaseCluster(self, "Database",
                                      engine=rds.DatabaseClusterEngine.aurora_postgres(
                                          version=rds.AuroraPostgresEngineVersion.VER_10_7),
                                      writer=rds.ClusterInstance.provisioned("writer",
                                                                             instance_type=ec2.InstanceType.of(
                                                                                 ec2.InstanceClass.R6G,
                                                                                 ec2.InstanceSize.XLARGE4)
                                                                             ),
                                      serverless_v2_min_capacity=6.5,
                                      serverless_v2_max_capacity=64,
                                      readers=[
                                          # will be put in promotion tier 1 and will scale with the writer
                                          rds.ClusterInstance.serverless_v2("reader1", scale_with_writer=True),
                                          # will be put in promotion tier 2 and will not scale with the writer
                                          rds.ClusterInstance.serverless_v2("reader2")
                                      ],
                                      vpc=vpc,
                                      removal_policy=RemovalPolicy.DESTROY,
                                      )

        CfnOutput(
            self,
            "ClusterEndpoint",
            value=cluster.cluster_endpoint.hostname + ':' + str(cluster.cluster_endpoint.port),
            description="The endpoint to use for read/write operations.",
        )
        CfnOutput(
            self,
            "ClusterIdentifier",
            value=cluster.cluster_identifier,
            description="Identifier of the cluster.",
        )

        CfnOutput(
            self,
            "ReaderEndpoint",
            value=cluster.cluster_read_endpoint.hostname + ':' + str(cluster.cluster_read_endpoint.port),
            description="Endpoint to use for load-balanced read-only operations.",
        )
        CfnOutput(
            self,
            "ResourceIdentifier",
            value=cluster.cluster_resource_identifier,
            description="This AWS Region-unique identifier is used in things like IAM authentication policies.",
        )
        CfnOutput(
            self,
            "EngineVersion",
            value=cluster.engine.engine_version.full_version,
            description="The engine version for this Cluster.",
        )
        CfnOutput(
            self,
            "EngineFamily",
            value=cluster.engine.engine_family,
            description="The engine family for this Cluster.",
        )
        CfnOutput(
            self,
            "EngineType",
            value=cluster.engine.engine_type,
            description="The engine type for this Cluster.",
        )
