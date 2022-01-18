from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw, CfnOutput,
)
from aws_solutions_constructs import (
    aws_apigateway_lambda as apigw_lambda
)
from constructs import Construct


class SolutionsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Fetch dummy Lambda function handler code
        with open("./assets/script.py", encoding="utf8") as fp:
            handler_code = fp.read()

        api = apigw_lambda.ApiGatewayToLambda(
            self, 'ApiGatewayToLambda',
            lambda_function_props=lambda_.FunctionProps(
                runtime=lambda_.Runtime.PYTHON_3_9,
                code=lambda_.InlineCode(handler_code),
                handler="index.main",
            ),
            api_gateway_props=apigw.RestApiProps(
                default_method_options=apigw.MethodOptions(
                    authorization_type=apigw.AuthorizationType.NONE
                )
            )
        )

        CfnOutput(self, "aws-apigateway-lambda-id",
                  value=api.api_gateway.rest_api_id,
                  description='The ID of this API Gateway RestApi.',
                  )
