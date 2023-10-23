from aws_cdk import (
    NestedStack, aws_ec2 as ec2, aws_rds as rds, RemovalPolicy, CfnOutput, )
from aws_cdk.aws_rds import CfnDBInstance
from constructs import Construct


class RdsNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc,
                 instance_type: ec2.InstanceType = ec2.InstanceType.of(ec2.InstanceClass.R5,
                                                                       ec2.InstanceSize.LARGE),
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 cluster_identifier: str = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        parameter_group = rds.ParameterGroup(self, "ParameterGroup",
                                             engine=rds.DatabaseInstanceEngine.postgres(
                                                 version=rds.PostgresEngineVersion.VER_15_3),
                                             description='Testing drift',
                                             parameters={
                                                 "shared_preload_libraries": "pg_stat_statements",
                                                 "track_activity_query_size": "4097"
                                             }
                                             )

        # option_group = rds.OptionGroup(self, "Options",
        #                 engine=rds.DatabaseInstanceEngine.oracle_se2(
        #                     version=rds.OracleEngineVersion.VER_19
        #                 ),
        #                 configurations=[rds.OptionConfiguration(
        #                     name="OEM",
        #                     port=5500,
        #                     vpc=vpc,
        #                     security_groups=[security_group]
        #                 )
        #                 ]
        #                 )

        cluster = rds.DatabaseCluster(self, "Database",
                                      cluster_identifier=cluster_identifier,
                                      engine=rds.DatabaseClusterEngine.aurora_postgres(
                                          version=rds.AuroraPostgresEngineVersion.VER_15_2),
                                      credentials=rds.Credentials.from_generated_secret(
                                          "syscdk"),
                                      instance_props=rds.InstanceProps(
                                          instance_type=instance_type,
                                          vpc_subnets=ec2.SubnetSelection(
                                              subnet_type=ec2.SubnetType.PUBLIC),
                                          vpc=vpc
                                      ),
                                      storage_type=rds.DBClusterStorageType.AURORA_IOPT1,
                                      removal_policy=removal_policy,
                                      )

        CfnOutput(self, 'DbClusterIdentifier',  value=cluster.cluster_identifier,
                  description='The cluster identifier.')

        instance = rds.DatabaseInstance(self, "Instance",
                                        engine=rds.DatabaseInstanceEngine.postgres(
                                            version=rds.PostgresEngineVersion.VER_15_3),
                                        # optional, defaults to m5.large
                                        instance_type=instance_type,
                                        credentials=rds.Credentials.from_generated_secret(
                                            "syscdk"),
                                        # Optional - will default to 'admin' username and generated password
                                        vpc=vpc,
                                        vpc_subnets=ec2.SubnetSelection(
                                            subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
                                        ),
                                        parameter_group=parameter_group,
                                        removal_policy=removal_policy,
                                        delete_automated_backups=(
                                            removal_policy == RemovalPolicy.DESTROY),
                                        )

        CfnOutput(self, 'DbInstanceIdentifier',
                  value=instance.instance_identifier,
                  description='The instance identifier.'
                  )
        CfnOutput(self, 'DbInstanceArn',
                  value=instance.instance_arn,
                  description='The instance arn.'
                  )

        CfnOutput(self, 'DbInstanceEndpointAddress',
                  value=instance.db_instance_endpoint_address,
                  description='The instance endpoint address.'
                  )
        CfnOutput(self, 'DbInstanceEndpointPort',
                  value=instance.db_instance_endpoint_port,
                  description='The instance endpoint port.'
                  )

        cfn_dBInstance = CfnDBInstance(self, "MyCfnDBInstance",
                                       engine="postgres",
                                       engine_version="15.3",

                                       db_instance_class="db.r5.large",
                                       allocated_storage="20",
                                       storage_type="gp2",

                                       master_username="syscdk",
                                       master_user_password="Wagw00rd",

                                       # ca_certificate_identifier="rds-ca-rsa2048-g1",
                                       # certificate_rotation_restart=False,
                                       )

        proxy = rds.DatabaseProxy(self, "Proxy",
            proxy_target=rds.ProxyTarget.from_cluster(cluster),
            secrets=[cluster.secret],
            vpc=vpc
        )
