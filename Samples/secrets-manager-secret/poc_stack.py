from aws_cdk import (
    core as cdk,
    aws_secretsmanager as sm,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class PocStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get a value from AWS Secrets Manager
        # https://docs.aws.amazon.com/cdk/latest/guide/get_secrets_manager_value.html

        secret = sm.Secret.from_secret_attributes(self, "ImportedSecret", secret_complete_arn="arn:aws:secretsmanager:<region>:<account-id-number>:secret:<secret-name>-<random-6-characters>",
        # If the secret is encrypted using a KMS-hosted CMK, either import or reference that key:
        # encryption_key=....
        )

        secret_value = secret.secret_value.to_string()

        cdk.CfnOutput(self, 'SecretValue',
        value=secret_value,
        description='Resolved Secret value.',
        )
