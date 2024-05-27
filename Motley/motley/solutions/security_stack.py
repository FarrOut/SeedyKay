from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, )
from constructs import Construct

from motley.components.security.secrets_stack import SecretsStack


class SecurityStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.secret = SecretsStack(self, "SecretsStack", removal_policy=removal_policy).secret
