from aws_cdk import (
    # Duration,
    Stack,
    aws_kms as kms, aws_ssm as ssm,
    CfnOutput, )
from constructs import Construct


class CrossAccountBuildStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, key_arn_param: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        key_arn = ssm.StringParameter.value_from_lookup(self, key_arn_param)

        # my_key_imported = kms.Key.from_key_arn(self, "MyImportedKey", key_arn)
        #
        # CfnOutput(self, 'KeyArn',
        #           description='ARN of this key.',
        #           value=my_key_imported.key_arn,
        #           )
