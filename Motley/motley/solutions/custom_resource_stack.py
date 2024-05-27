from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, aws_ec2 as ec2, custom_resources as cr, aws_iam as iam,)
from constructs import Construct
import time
from motley.components.custom.customer_resources_nestedstack import CustomResourceNestedStack


class CustomResourceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc_endpoint: ec2.IInterfaceVpcEndpoint,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stack = CustomResourceNestedStack(
            self, "CustomResourceNestedStack", vpc_endpoint=vpc_endpoint, removal_policy=removal_policy)


