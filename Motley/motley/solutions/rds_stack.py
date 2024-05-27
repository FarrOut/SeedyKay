from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, aws_ec2 as ec2, aws_rds as rds,)
from constructs import Construct
from motley.components.storage.databases.rds_nestedstack import RdsNestedStack
from motley.components.storage.databases.rds_tagged_nest import RdsTaggedNest


class RdsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        RdsNestedStack(self, "RdsNestedStack", vpc=vpc,
                       removal_policy=removal_policy)

        # RdsTaggedNest(self, "RdsTaggedNest", vpc=vpc,
        #                removal_policy=removal_policy)
