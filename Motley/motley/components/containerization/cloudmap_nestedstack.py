from aws_cdk import (
    Duration,
    NestedStack, aws_servicediscovery as servicediscovery, aws_elasticloadbalancingv2 as elbv2,
    aws_ecr as ecr, aws_ec2 as ec2, CfnOutput, RemovalPolicy, )
from aws_cdk.aws_ecs import ContainerImage, RepositoryImage
from aws_cdk.aws_secretsmanager import ISecret
from aws_cdk.aws_sns import Topic
from constructs import Construct


class CloudMapNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        namespace = servicediscovery.HttpNamespace(self, "MyNamespace",
                                                   name="MyHTTPNamespace"
                                                   )
        namespace.apply_removal_policy(removal_policy)

        self.service = namespace.create_service("Service",
                                                # health_check=servicediscovery.HealthCheckConfig(
                                                #     type=servicediscovery.HealthCheckType.HTTP,
                                                #     resource_path="/check"
                                                # ),
                                                custom_health_check=servicediscovery.HealthCheckCustomConfig(
                                                    failure_threshold=3,
                                                ),
                                                )
        self.service.apply_removal_policy(removal_policy)
        instance = self.service.register_non_ip_instance('NationalService', custom_attributes={
            "attribute": "custom"
        })
        instance.apply_removal_policy(removal_policy)

        # loadbalancer = elbv2.ApplicationLoadBalancer(
        #     self, "LB", vpc=vpc, internet_facing=True)
        # loadbalancer.apply_removal_policy(removal_policy)

        # self.service.register_load_balancer("Loadbalancer", loadbalancer)

        CfnOutput(self, 'DiscoveryType', value=str(self.service.discovery_type),
                  description='The discovery type used by this service.')
        CfnOutput(self, 'DnsRecordType', value=str(self.service.dns_record_type),
                  description='The DnsRecordType used by the service.')
        CfnOutput(self, 'Namespace', value=str(self.service.namespace),
                  description='The namespace for the Cloudmap Service.')
        CfnOutput(self, 'RoutingPolicy', value=str(self.service.routing_policy),
                  description='The Routing Policy used by the service.')
        CfnOutput(self, 'ServiceArn', value=str(self.service.service_arn),
                  description='The Arn of the namespace that you want to use for DNS configuration.')
        CfnOutput(self, 'ServiceId', value=str(self.service.service_id),
                  description='The ID of the namespace that you want to use for DNS configuration.')
        CfnOutput(self, 'ServiceName', value=str(self.service.service_name),
                  description='A name for the Cloudmap Service.')
