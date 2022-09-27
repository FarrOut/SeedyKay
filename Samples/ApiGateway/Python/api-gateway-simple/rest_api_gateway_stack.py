from aws_cdk import (core as cdk,
aws_apigateway as apigateway,
aws_ec2 as ec2,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class RestApiGatewayStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.SpecRestApi(self, "ExampleRestApi",
            api_definition=apigateway.ApiDefinition.from_asset("assets\petstore_api_definition.json"),
        )
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-from-example.html

        cdk.CfnOutput(self, 'ApiGatewayNameOutput',
            value=api.rest_api_name,
            description='API Gataway Name',
        )

        deployment = apigateway.Deployment(self, 'Deployment',
            api=api,
        )
        api_stage = apigateway.Stage(self,'Stage',
            deployment=deployment, stage_name='stageA',
        )
        api.deployment_stage = api_stage
