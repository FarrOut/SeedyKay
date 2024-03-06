from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2,
    RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_ecs import ContainerImage
from constructs import Construct
from motley.components.security.ssm_document_nestedstack import SsmDocumentNestedStack

from motley.components.events.alarms_nestedstack import AlarmsNestedStack


class VpcEndpointStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.IVpc,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,                 
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        CfnOutput(self, "VpcId", value=vpc.vpc_id)


        endpoint = vpc.add_interface_endpoint('InterfaceEndpoint',
                                              service=ec2.InterfaceVpcEndpointAwsService('ssm'),
                                              open=False,                                              
                                              )
        endpoint.apply_removal_policy(removal_policy)

        CfnOutput(self, "EndpointId", value=endpoint.vpc_endpoint_id)
