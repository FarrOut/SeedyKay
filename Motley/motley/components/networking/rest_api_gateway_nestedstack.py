from aws_cdk import (
    # Duration,
    NestedStack, aws_cloudfront as cloudfront, aws_cloudfront_origins as origins, aws_s3 as s3,
    aws_s3_deployment as s3deploy, aws_apigateway as apigateway,
    RemovalPolicy, aws_elasticloadbalancingv2 as elbv2, aws_ec2 as ec2, CfnOutput, )
from constructs import Construct
from aws_cdk.aws_apigateway import MockIntegration, IntegrationResponse, MethodResponse, PassthroughBehavior, RestApi, RequestAuthorizer, IdentitySource


class RestApiGatewayNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.SpecRestApi(self, "ExampleRestApi",
                                     api_definition=apigateway.ApiDefinition.from_asset(
                                         "assets/api-gateway/petstore_api_definition.json"),
                                     )
        api.apply_removal_policy = removal_policy
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-from-example.html

        CfnOutput(self, 'ApiGatewayNameOutput',
                  value=api.rest_api_name,
                  description='API Gataway Name',
                  )

        deployment = apigateway.Deployment(self, 'Deployment',
                                           api=api,
                                           )
        deployment.apply_removal_policy = removal_policy
        api_stage = apigateway.Stage(self, 'Stage',
                                     deployment=deployment, stage_name='stageA',
                                     )
        api_stage.apply_removal_policy = removal_policy
        api.deployment_stage = api_stage

        v1 = api.root.add_resource("v1")
        echo = v1.add_resource("echo")
        integration = MockIntegration(
            integration_responses=[IntegrationResponse(status_code="200")
                                   ])
        method = echo.add_method("GET", integration, method_responses=[MethodResponse(
            status_code="200",
            response_parameters={
                "method.response.header.Access-Control-Allow-Origin": False
            }
        )], api_key_required=False)

        CfnOutput(self, 'MethodArn',
                  value=method.method_arn,
                  description='an execute-api ARN for this method',
                  )
        CfnOutput(self, 'MethodId',
                  value=method.method_id,
                  )
