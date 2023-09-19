from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_ecs import ContainerImage
from constructs import Construct

from motley.components.security.secrets_stack import SecretsStack

import boto3


class SecurityStack(Stack):
    special_tag = 'app-wide'

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        def __is_exists(filter_tag: str = SecurityStack.special_tag, region: str = self.region) -> bool:
            print(f'Looking up SecurityGroups in \'{region}\' region.')
            session = boto3.Session(profile_name='default', region_name=region)
            ec2_client = session.client('ec2')

            response = ec2_client.describe_security_groups(
                Filters=[
                    {
                        'Name': 'tag-key',
                        'Values': [
                            filter_tag,
                        ]
                    },
                ],
                # GroupIds=[
                #     'string',
                # ],
                # GroupNames=[
                #     'string',
                # ],
                # DryRun=False,
                # NextToken='string',
                # MaxResults=123
            )
            print(f'number of results ------------------> {len(response["SecurityGroups"])}')

            return len(response["SecurityGroups"]) > 0

        self.secret = SecretsStack(self, "SecretsStack", removal_policy=removal_policy).secret
