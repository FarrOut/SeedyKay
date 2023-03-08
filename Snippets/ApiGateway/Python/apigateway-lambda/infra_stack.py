from aws_cdk import (
    # Duration,
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as lambda_, CfnOutput,
)
from aws_cdk.aws_apigateway import LambdaIntegration
from constructs import Construct


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Fetch dummy Lambda function handler code
        with open("./assets/script.py", encoding="utf8") as fp:
            handler_code = fp.read()

        func_one = lambda_.Function(self, "func_one",
                                    runtime=lambda_.Runtime.PYTHON_3_9,
                                    handler="index.main",
                                    code=lambda_.InlineCode(handler_code),
                                    )

        api = apigateway.RestApi(self, "hello-api")
        self.rest_api_root_resource_id = api.rest_api_root_resource_id

        request_json_schema = apigateway.JsonSchema(
            schema=apigateway.JsonSchemaVersion.DRAFT4,
            title="Map",
            type=apigateway.JsonSchemaType.OBJECT,
            additional_properties=apigateway.JsonSchema(
                type=apigateway.JsonSchemaType.OBJECT,
                ref="#/definitions/Car",
            ),
            definitions=dict(Car=apigateway.JsonSchema(
                type=apigateway.JsonSchemaType.OBJECT,
                additional_properties=False,
                properties=dict(
                    model_code=apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.STRING,
                    ),
                    part_types=apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.OBJECT,
                        additional_properties=dict(
                            # ref="#/definitions/PartInfo",
                        ),
                    )
                ),
            )),
        )

        self.request_model = api.add_model("room-api-getContent-request",
                                           content_type="application/json",
                                           model_name="getContentRequest",
                                           schema=request_json_schema)

        resource = api.root.add_resource("v1")

        lambda_backend = LambdaIntegration(func_one)
        resource.add_method("GET", api_key_required=True,
                            request_validator=apigateway.RequestValidator(
                                scope=self,
                                rest_api=api,
                                id="api-validator",
                                request_validator_name="api-validator" + '-' + self.stack_name,
                                validate_request_body=True
                            ),
                            integration=lambda_backend,
                            request_models={
                                "application/json": self.request_model
                            })

        self.rest_api_id = api.rest_api_id
        CfnOutput(self, "RestApiId",
                  value=self.rest_api_id,
                  description='The ID of this API Gateway RestApi.',
                  )
