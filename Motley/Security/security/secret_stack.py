from aws_cdk import (
    # Duration,
    Stack,
    aws_secretsmanager as secretsmanager, CfnOutput, )
from aws_cdk.aws_sns import Topic
from constructs import Construct


class SecretStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        secret = secretsmanager.Secret(
            self,
            "TopSecret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template="{}",
                generate_string_key="auth_token",
                password_length=48,
                exclude_characters="':^,()@/",
                exclude_punctuation=True,
            ),
        )

        # How to resolve SecretValue
        secret_value = str(secret.secret_value_from_json("auth_token").unsafe_unwrap())

        dummy = Topic(self, 'Dummy',
                      topic_name=secret_value
                      )
        CfnOutput(self, 'SecretValue',
                  description='Resolved secret value',
                  value=dummy.topic_name
                  )
