from aws_cdk import (
    NestedStack, aws_ec2 as ec2, aws_rds as rds, RemovalPolicy, Tags,  CfnOutput, )
from aws_cdk.aws_rds import CfnDBInstance
from constructs import Construct


class RdsTaggedNest(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 cluster_identifier: str = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cluster = rds.DatabaseCluster(self, "Database",
                                      cluster_identifier=cluster_identifier,
                                      engine=rds.DatabaseClusterEngine.aurora_postgres(
                                          version=rds.AuroraPostgresEngineVersion.VER_13_12),
                                      credentials=rds.Credentials.from_generated_secret(
                                          "syscdk"),
                                      storage_type=rds.DBClusterStorageType.AURORA_IOPT1,
                                      removal_policy=removal_policy,
                                      vpc=vpc,
                                      writer=rds.ClusterInstance.provisioned("writer",
                                                          instance_type=ec2.InstanceType.of(
                                                              ec2.InstanceClass.R6G, ec2.InstanceSize.LARGE)
                                                          ),
                                      readers=[rds.ClusterInstance.serverless_v2(
                                          "reader1", scale_with_writer=True),],
                                      )

        CfnOutput(self, 'DbClusterIdentifier',  value=cluster.cluster_identifier,
                  description='The cluster identifier.')

        cfn_cluster = cluster.node.default_child
        Tags.of(cfn_cluster).add("Note", "tag added")

