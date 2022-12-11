from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_kms as kms,
    aws_redshift as redshift, RemovalPolicy,
)
from aws_cdk.aws_redshift import CfnCluster
from constructs import Construct


class RedshiftStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        key = kms.Key(self, "MyKey",
                      removal_policy=RemovalPolicy.DESTROY,
                      )

        cluster = CfnCluster(self, 'Cluster',
                             cluster_type='single-node',
                             db_name='dev',
                             master_username='bevelvoerder',
                             master_user_password='Wagw00rdEen',
                             node_type='dc2.large',
                             encrypted=True,
                             kms_key_id=key.key_id,
                             classic=True,
                             )
        cluster.apply_removal_policy(RemovalPolicy.DESTROY)
