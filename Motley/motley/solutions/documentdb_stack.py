from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, )
from constructs import Construct


class DocumentDbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # self.docdb = DocDbNestedStack(self, "DocDbNestedStack", removal_policy=removal_policy)
