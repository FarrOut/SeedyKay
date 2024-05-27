from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy,aws_sns as sns,
)
from constructs import Construct

from motley.components.security.compliance.config_nestedstack import ConfigNestedStack


class ConfigStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ConfigNestedStack(self, 'ConfigNestedStack',        
                                           removal_policy=removal_policy,
                                           )

        burner =  sns.Topic(self, 'Burner',
                           display_name='Burner',
                           topic_name='Burner',
                           )
        burner.apply_removal_policy(removal_policy)