from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ec2 as ec2, aws_rds as rds,aws_kms as kms,
    aws_secretsmanager as secretsmanager, RemovalPolicy, CfnOutput, PhysicalName, )
from aws_cdk.aws_rds import Credentials
from constructs import Construct


class SecretsStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        key = kms.Key(self, "KMS", removal_policy=removal_policy)

        self.secret = secretsmanager.Secret(
            self,
            "TopSecret",
            secret_name=f"cross-environment-secret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template="{\"username\": \"commander\"}",
                generate_string_key="password",
                password_length=10,
                exclude_characters="':^,()@/",
                exclude_punctuation=True,
            ),
            removal_policy=removal_policy,
            encryption_key=key,
        )

        CfnOutput(self, 'SecretName', value=self.secret.secret_name,
                  description='The name of the Secret resource.')
        CfnOutput(self, 'SecretFullArn', value=self.secret.secret_full_arn,
                  description='The full ARN of the Secret resource.')
        CfnOutput(self, 'SecretArn', value=self.secret.secret_arn,
                  description='The ARN of the Secret resource.')

        ### How to resolve SecretValue ###
        # secret_value = str(secret.secret_value_from_json("password").unsafe_unwrap())
        #
        # dummy = Topic(self, 'Dummy',
        #               topic_name=secret_value
        #               )
        # CfnOutput(self, 'SecretValue',
        #
        #           description='Resolved secret value',
        #           value=dummy.topic_name
        #           )
