from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2, aws_logs as logs,
    aws_elasticache as elasticache,
    CfnOutput, RemovalPolicy, )
from constructs import Construct


class ElastiCacheStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, log_group: logs.LogGroup, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        subnet_group = elasticache.CfnSubnetGroup(self, "SubnetGroup",
                                                  description="Subnet group for Redis caches",
                                                  subnet_ids=[vpc.private_subnets[0].subnet_id,
                                                              vpc.private_subnets[1].subnet_id],

                                                  # the properties below are optional
                                                  cache_subnet_group_name="redis-cache-subnet-group",
                                                  )
        CfnOutput(self, 'SubnetGroupName',
                  value=str(subnet_group.cache_subnet_group_name),
                  description='The name for the cache subnet group. This value is stored as a lowercase string.'
                  )
        CfnOutput(self, 'SubnetGroupDescription',
                  value=str(subnet_group.description),
                  description='The description for the cache subnet group.'
                  )
        CfnOutput(self, 'SubnetGroupRef',
                  value=str(subnet_group.ref),
                  description='The Ref intrinsic function, Ref returns the resource name. '
                  )

        sec_grp_one = ec2.SecurityGroup(self, "SecurityGroupOne",
                                        vpc=vpc,
                                        description="ElastiCache testing security group one.",
                                        allow_all_outbound=True
                                        )
        sec_grp_one.apply_removal_policy(RemovalPolicy.DESTROY)

        sec_grp_two = ec2.SecurityGroup(self, "SecurityGroupTwo",
                                        vpc=vpc,
                                        description="ElastiCache testing security group two.",
                                        allow_all_outbound=False,
                                        )
        sec_grp_two.apply_removal_policy(RemovalPolicy.DESTROY)

        # cluster = elasticache.CfnCacheCluster(self, "MyCfnCacheCluster",
        #                                       auto_minor_version_upgrade=False,
        #                                       az_mode='cross-az',
        #                                       cache_node_type='cache.t3.medium',
        #                                       engine='redis',
        #                                       engine_version='6.2',
        #                                       num_cache_nodes=2,
        #                                       log_delivery_configurations=[
        #                                           elasticache.CfnCacheCluster.LogDeliveryConfigurationRequestProperty(
        #                                               destination_details=elasticache.CfnCacheCluster.DestinationDetailsProperty(
        #                                                   cloud_watch_logs_details=elasticache.CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty(
        #                                                       log_group=log_group.log_group_name,
        #                                                   ),
        #
        #                                               ),
        #                                               destination_type="cloudwatch-logs",
        #                                               log_format="text",
        #                                               log_type="slow-log"
        #                                           ),
        #                                           elasticache.CfnCacheCluster.LogDeliveryConfigurationRequestProperty(
        #                                               destination_details=elasticache.CfnCacheCluster.DestinationDetailsProperty(
        #                                                   cloud_watch_logs_details=elasticache.CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty(
        #                                                       log_group=log_group.log_group_name,
        #                                                   ),
        #
        #                                               ),
        #                                               destination_type="cloudwatch-logs",
        #                                               log_format="text",
        #                                               log_type="engine-log"
        #                                           )],
        #                                       cache_subnet_group_name=subnet_group.ref,
        #                                       preferred_maintenance_window="sun:07:00-sun:08:00",
        #                                       transit_encryption_enabled=True,
        #                                       vpc_security_group_ids=[sec_grp_one.security_group_id,
        #                                                               sec_grp_two.security_group_id],
        #                                       )
        #
        # CfnOutput(self, 'ClusterName',
        #           value=str(cluster.cluster_name),
        #           description='A name for the cache cluster.'
        #           )
        # CfnOutput(self, 'ClusterRef',
        #           value=str(cluster.ref),
        #           description='The Ref intrinsic function, Ref returns the resource name. '
        #           )

        replication_group = elasticache.CfnReplicationGroup(self, "MyCfnReplicationGroup",
                                                            replication_group_description='TestReplicationGroup',
                                                            engine='redis',
                                                            engine_version='6.2',
                                                            cluster_mode='enabled',
                                                            cache_node_type='cache.t3.medium',
                                                            multi_az_enabled=True,
                                                            num_cache_clusters=2,
                                                            cache_subnet_group_name=subnet_group.ref,
                                                            log_delivery_configurations=[
                                                                elasticache.CfnReplicationGroup.LogDeliveryConfigurationRequestProperty(
                                                                    destination_details=elasticache.CfnReplicationGroup.DestinationDetailsProperty(
                                                                        cloud_watch_logs_details=elasticache.CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty(
                                                                            log_group=log_group.log_group_name,
                                                                        ),

                                                                    ),
                                                                    destination_type="cloudwatch-logs",
                                                                    log_format="text",
                                                                    log_type="slow-log"
                                                                ),
                                                                elasticache.CfnReplicationGroup.LogDeliveryConfigurationRequestProperty(
                                                                    destination_details=elasticache.CfnReplicationGroup.DestinationDetailsProperty(
                                                                        cloud_watch_logs_details=elasticache.CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty(
                                                                            log_group=log_group.log_group_name,
                                                                        ),

                                                                    ),
                                                                    destination_type="cloudwatch-logs",
                                                                    log_format="text",
                                                                    log_type="engine-log"
                                                                )],
                                                            preferred_maintenance_window="sun:07:00-sun:08:00",
                                                            transit_encryption_enabled=False,
                                                            )

        CfnOutput(self, 'ReplicationGroupRef',
                  value=str(replication_group.ref),
                  description='The Ref intrinsic function, Ref returns the resource name. '
                  )
        CfnOutput(self, 'ReplicationGroupClusterMode',
                  value=str(replication_group.cluster_mode),
                  description='Enabled or Disabled.'
                  )
        CfnOutput(self, 'ReplicationGroupEngine',
                  value=str(replication_group.engine),
                  description='The name of the cache engine to be used for the clusters in this replication group.'
                  )
        CfnOutput(self, 'ReplicationGroupEngineVersion',
                  value=str(replication_group.engine_version),
                  description='The version number of the cache engine to be used for the clusters in this replication '
                              'group.'
                  )
        CfnOutput(self, 'ReplicationGroupGlobalId',
                  value=str(replication_group.global_replication_group_id),
                  description='The name of the Global datastore.'
                  )
        CfnOutput(self, 'ReplicationGroupMultiAzEnabled',
                  value=str(replication_group.multi_az_enabled),
                  description='A flag indicating if you have Multi-AZ enabled to enhance fault tolerance.'
                  )
        CfnOutput(self, 'ReplicationGroupNetworkType',
                  value=str(replication_group.network_type),
                  description='Must be either ipv4 | ipv6 | dual_stack .'
                  )
