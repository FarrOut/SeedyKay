from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, aws_ec2 as ec2,)
from constructs import Construct
from motley.components.storage.databases.rds_nestedstack import RdsNestedStack


class RdsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        RdsNestedStack(self, "RdsNestedStack", vpc=vpc,
                       removal_policy=removal_policy)
