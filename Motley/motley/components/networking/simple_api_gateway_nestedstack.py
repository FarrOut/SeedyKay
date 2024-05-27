from aws_cdk import (
    # Duration,
    NestedStack, aws_cloudfront as cloudfront, aws_cloudfront_origins as origins, aws_s3 as s3,
    aws_s3_deployment as s3deploy, aws_apigateway as apigateway, aws_lambda as lambda_,
    RemovalPolicy, aws_elasticloadbalancingv2 as elbv2, aws_ec2 as ec2, CfnOutput, )
from constructs import Construct
from aws_cdk.aws_apigateway import MockIntegration, IntegrationResponse, MethodResponse, PassthroughBehavior, RestApi, RequestAuthorizer, IdentitySource

from motley.computing.lambda_nestedstack import LambdaNestedStack
import time


class SimpleApiGatewayNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.RestApi(self, "simple-api",
                                 rest_api_name='SimpleApi',
                                 endpoint_types=[
                                     apigateway.EndpointType.REGIONAL],
                                 deploy=True,
                                 deploy_options=apigateway.StageOptions(
                                     stage_name='dev',
                                     description=f'Pretty fly...for an API.',
                                 ),
                                 default_method_options=apigateway.MethodOptions(
                                     authorization_type=apigateway.AuthorizationType.IAM,
                                 ),
                                 )
        api.apply_removal_policy = removal_policy
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-from-example.html

        CfnOutput(self, 'ApiGatewayNameOutput',
                  value=api.rest_api_name,
                  description='API Gataway Name',
                  )
        CfnOutput(self, 'ApiGatewayIdOutput',
                  value=api.rest_api_id,
                  description='The ID of this API Gateway RestApi.',
                  )

        sample_resource_1 = api.root.add_resource("sampleResource1")
        func_1 = lambda_.Function(self, "lambda_function_one",
                                  runtime=lambda_.Runtime.PYTHON_3_12,
                                  handler="lambda_handler.lambda_handler",
                                  code=lambda_.Code.from_asset(
                                      "./assets/api-gateway"),
                                  )
        func_1.apply_removal_policy(removal_policy)
        method_1 = sample_resource_1.add_method(
            "POST", apigateway.LambdaIntegration(func_1, proxy=True,),)

        CfnOutput(self, 'Method1Arn',
                  value=method_1.method_arn,
                  description='an execute-api ARN for this method',
                  )
        CfnOutput(self, 'Method1Id',
                  value=method_1.method_id,
                  )

        # sample_resource_2 = api.root.add_resource("sampleResource2")
        # func_2 = lambda_.Function(self, "lambda_function_two",
        #                           runtime=lambda_.Runtime.PYTHON_3_12,
        #                           handler="lambda_handler.lambda_handler",
        #                           code=lambda_.Code.from_asset(
        #                               "./assets/api-gateway"),
        #                           )
        # func_2.apply_removal_policy(removal_policy)
        # method_2 = sample_resource_2.add_method(
        #     "POST", apigateway.LambdaIntegration(func_2, proxy=True,),)
        # CfnOutput(self, 'Method2Arn',
        #           value=method_2.method_arn,
        #           description='an execute-api ARN for this method',
        #           )
        # CfnOutput(self, 'Method2Id',
        #           value=method_2.method_id,
        #           )

        latest_deployment = api.latest_deployment

        CfnOutput(self, 'TimeNow',
                  value=str(time.time()),
                  )

        if latest_deployment is not None:
            latest_deployment.add_to_logical_id(
                time.time())
            CfnOutput(self, 'LatestDeploymentId',
                      value=str(latest_deployment.deployment_id),
                      )

        stage = api.deployment_stage

        # deployment = apigateway.Deployment(self, "Deployment", api=api,
        #                                    # When an API Gateway model is updated, a new deployment will automatically be created.
        #                                    retain_deployments=False,
        #                                    )
        # deployment.add_to_logical_id(time.time())
        # deployment.node.add_dependency(sample_resource_1)
        # deployment.node.add_dependency(sample_resource_2)

        # stage = apigateway.Stage(self, "dev",
        #                          deployment=deployment,
        #                          stage_name='dev',
        #                          )
        CfnOutput(self, 'StageName',
                  value=stage.stage_name,
                  )
        CfnOutput(self, 'StageArn',
                  value=stage.stage_arn,
                  )
