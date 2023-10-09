from aws_cdk import (
    # Duration,
    NestedStack, aws_s3 as s3,
    aws_ssm as ssm, RemovalPolicy, CfnOutput, )
from constructs import Construct


class SsmDocumentNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.doc = ssm.CfnDocument(self, "SsmDocument", document_type="Command", content={
            "schemaVersion": "2.2",
            "description": "SSM Document",
            "mainSteps": [
                {
                    "name": "Test",
                    "action": "aws:runPowerShellScript",
                    "precondition": {
                        "StringEquals": [
                            "platformType",
                            "Windows"
                        ]
                    },
                    "inputs": {
                        "runCommand": [
                            "echo \"Test\""
                        ]
                    }
                }
            ]
        },

        )
        self.doc.apply_removal_policy(removal_policy)

        CfnOutput(self, 'DocumentName',
                  description='A name for the SSM document.',
                  value=str(self.doc.name)
                  )
