from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy,
)
from constructs import Construct
from motley.components.networking.rest_api_gateway_nestedstack import RestApiGatewayNestedStack
from motley.components.networking.simple_api_gateway_nestedstack import SimpleApiGatewayNestedStack


class ApiGatewayStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # api_gw = RestApiGatewayNestedStack(self, 'RestApiGatewayNestedStack',        
        #                                    removal_policy=removal_policy,
        #                                    )

        api_gw = SimpleApiGatewayNestedStack(self, 'SimpleApiGatewayNestedStack',        
                                           removal_policy=removal_policy,
                                           )