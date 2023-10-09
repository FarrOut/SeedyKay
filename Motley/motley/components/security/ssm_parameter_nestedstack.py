from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ssm as ssm, RemovalPolicy, CfnOutput, )
from constructs import Construct


class SsmParameterNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.param = ssm.StringParameter(self, "Parameter",
                                    allowed_pattern=".*",
                                    description="The value Foo",
                                    parameter_name="FooParameter",
                                    string_value="Foo",
                                    tier=ssm.ParameterTier.STANDARD
                                    )
        self.param.apply_removal_policy(RemovalPolicy.DESTROY)

        CfnOutput(self, 'ParameterArn',
                  description='The ARN of the SSM Parameter resource.',
                  value=self.param.parameter_arn
                  )
        CfnOutput(self, 'ParameterName',
                  description='The name of the SSM Parameter resource.',
                  value=self.param.parameter_name
                  )
        CfnOutput(self, 'ParameterType',
                  description='The type of the SSM Parameter resource.',
                  value=self.param.parameter_type
                  )
        CfnOutput(self, 'ParameterStringValue',
                  description='The parameter value.',
                  value=self.param.string_value
                  )
