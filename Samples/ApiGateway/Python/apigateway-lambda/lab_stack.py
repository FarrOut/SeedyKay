from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_apigateway as apigateway,
    aws_lambda as lambda_, CfnOutput,
)
from aws_cdk.aws_apigateway import RestApi, Model, LambdaIntegration
from constructs import Construct


class LabStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, rest_api_id: str, request_model: Model,
                 rest_api_root_resource_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/RestApi.html#aws_cdk.aws_apigateway.RestApi.from_rest_api_id
        imported_api = RestApi.from_rest_api_attributes(self, 'ImportedRestApi',
                                                        rest_api_id=rest_api_id,
                                                        root_resource_id=rest_api_root_resource_id,
                                                        )
        CfnOutput(self, "ImportedRestApiId",
                  value=imported_api.rest_api_id,
                  description='The ID of this (imported) API Gateway RestApi.',
                  )

        # Fetch dummy Lambda function handler code
        with open("./assets/script.py", encoding="utf8") as fp:
            handler_code = fp.read()
        func_two = lambda_.Function(self, "func_two",
                                    runtime=lambda_.Runtime.PYTHON_3_9,
                                    handler="index.main",
                                    code=lambda_.InlineCode(handler_code),
                                    )

        # Now let's swap out the function with a sandbox!
        new_lambda_backend = LambdaIntegration(func_two)
        resource = imported_api.root.add_resource("v2")

        resource.add_method("GET", api_key_required=True,
                            request_validator=apigateway.RequestValidator(
                                scope=self,
                                rest_api=imported_api,
                                id="api-validator",
                                request_validator_name="api-validator" + '-' + self.stack_name,
                                validate_request_body=True
                            ),
                            integration=new_lambda_backend,
                            request_models={
                                "application/json": request_model
                            })

        rest_api_id = imported_api.rest_api_id
        CfnOutput(self, "RestApiId",
                  value=rest_api_id,
                  description='The ID of this API Gateway RestApi.',
                  )
