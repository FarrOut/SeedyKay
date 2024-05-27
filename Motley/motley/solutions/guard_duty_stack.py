from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy,aws_sns as sns,
)
from constructs import Construct

from motley.components.security.compliance.config_nestedstack import ConfigNestedStack
from motley.components.security.guard_duty_nest import GuardDutyNest


class GuardDutyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        GuardDutyNest(self, 'GuardDutyNest',        
                                           removal_policy=removal_policy,
                                           )

        # burner =  sns.Topic(self, 'Burner',
        #                    display_name='Burner',
        #                    topic_name='Burner',
        #                    )
        # burner.apply_removal_policy(removal_policy)