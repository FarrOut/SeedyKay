from aws_cdk import (
    # Duration,
    NestedStack, aws_cloudwatch as cloudwatch, aws_iot as iot, aws_iam as iam, aws_lambda as lambda_, aws_s3_assets as assets, custom_resources as cr, aws_ec2 as ec2, aws_s3 as s3, aws_s3_deployment as s3deploy, Fn,
    RemovalPolicy, CfnOutput, Tags, )
from constructs import Construct

from motley.components.iot.iot_logging_nestedstack import IoTloggingNestedStack
from motley.components.iot.iot_rules_nestedstack import IoTRulesNestedStack
from motley.components.storage.block.s3_stack import S3NestedStack
from motley.computing.lambda_nestedstack import LambdaNestedStack
import time
import json


class CustomResourceNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc_endpoint: ec2.IInterfaceVpcEndpoint, removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # iam.Role.customize_roles(self,
        #                          prevent_synthesis=True,
        #                          use_precreated_roles={
        #                              'CustomResourceStack/CustomResourceNestedStack/AWSCDKCfnUtilsProviderCustomResourceProvider/Role': 'my-custom-role',
        #                              'CustomResourceStack/CustomResourceNestedStack/customresourcerole': 'customresource-servicerole',
        #                          }
        #                          )

        # role = iam.Role(self, "ServiceRole",
        #                 assumed_by=iam.ServicePrincipal(
        #                     "lambda.amazonaws.com"),
        #                 description="The role used for the function."
        #                 )

        # asset = assets.Asset(self, "SampleAsset",    path="./assets/handlers")

        # self.function = lambda_.Function(self, "handler",
        #                                  runtime=lambda_.Runtime.PYTHON_3_12,
        #                                  handler="custom_resource.handler",
        #                                  role=role,
        #                                  code=asset,
        #                                  )
        # self.function.apply_removal_policy(removal_policy)

        customresource_role = iam.Role(
            self, "customresourcerole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="This role is for AWS custom resource",
            role_name=f"custom-{self.stack_name}customresource_role",
        )

        customresource_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["ec2:DescribeNetworkInterfaces"],
                resources=["*"]
            )
        )
        # customresource_role.apply_removal_policy(removal_policy)

        network_ids = vpc_endpoint.vpc_endpoint_network_interface_ids

        self.eni = cr.AwsCustomResource(
            self, "describenetworkinterfaces",
            install_latest_aws_sdk=True,
            on_create=cr.AwsSdkCall(
                service="EC2",
                action="describeNetworkInterfaces",
                parameters={
                    # "NetworkInterfaceIds": json.loads(vpc_endpoint.vpc_endpoint_network_interface_ids)
                    "NetworkInterfaceIds": network_ids
                },
                physical_resource_id=cr.PhysicalResourceId.of(
                    str(time.time())),
            ),
            role=customresource_role
        )

        # CfnOutput(self, 'NetworkInterfaceIds',
        #           value=json.loads(
        #               vpc_endpoint.vpc_endpoint_network_interface_ids),
        #           )

        # CfnOutput(self, 'NetworkInterfaceIdsTypeOf',
        #     value=type(vpc_endpoint.vpc_endpoint_network_interface_ids),
        #     )

        # print(f'Network IDs: {network_ids}')

        # for resource in network_ids.node.find_all():
        #     print(f'{resource.node.id} -- {resource.node.children}')

        # child = self.node.try_find_child('AWSCDKCfnUtilsProviderCustomResourceProviderRoleFE0EE867')
        # print(f'Child: {child}')
