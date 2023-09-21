from aws_cdk import (
    # Duration,
    Stack,
    Tags,
    aws_kinesis as kinesis,
    CfnOutput,
    RemovalPolicy,
    Duration,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_opensearchservice as opensearch,
)
from constructs import Construct
from aws_cdk.aws_opensearchservice import (
    EngineVersion,
    CapacityConfig,
    EbsOptions,
    ZoneAwarenessConfig,
    LoggingOptions,
    EncryptionAtRestOptions,
)


class OpenSearchStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        version: EngineVersion,
        vpc: ec2.IVpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(
            self, "opensearch-role", assumed_by=iam.ServicePrincipal("es.amazonaws.com")
        )
        CfnOutput(
            self,
            "roleArn",
            value=role.role_arn,
            description="Arn of the Amazon OpenSearch Service role.",
        )

        self.domain = opensearch.Domain(
            self,
            "Domain",
            version=version,
            capacity=CapacityConfig(master_nodes=3, data_nodes=10),
            ebs=EbsOptions(volume_size=20),
            zone_awareness=ZoneAwarenessConfig(availability_zone_count=3),
            logging=LoggingOptions(
                slow_search_log_enabled=True,
                app_log_enabled=True,
                slow_index_log_enabled=True,
            ),
            enforce_https=True,
            encryption_at_rest=EncryptionAtRestOptions(enabled=True),
            node_to_node_encryption=True,
            # vpc=vpc,
            advanced_options={
                "rest.action.multi.allow_explicit_index": "true",
                "override_main_response_version": "true",
            },
            enable_version_upgrade=True,
            removal_policy=RemovalPolicy.DESTROY,
        )
        self.domain.grant_read_write(role)

        Tags.of(self.domain).add("Message", "Upgrading to version 1.3")

        access_policy = iam.PolicyStatement(
            principals=[iam.AnyPrincipal()],
            actions=["es:*"],
            resources=[
                f"arn:aws:es:{self.region}:{self.account}:domain/{self.domain.domain_name}/*"
            ],
            effect=iam.Effect.ALLOW,
            conditions={
                "IpAddress": {
                    "aws:SourceIp": [
                        "10.0.0.0/8",
                    ]
                }
            },
        )
        self.domain.add_access_policies(access_policy)

        CfnOutput(
            self,
            "DomainName",
            value=self.domain.domain_name,
            description="LoggingOptions",
        )

        CfnOutput(
            self,
            "DomainArn",
            value=self.domain.domain_arn,
            description="Arn of the Amazon OpenSearch Service domain.",
        )

        CfnOutput(
            self,
            "DomainId",
            value=self.domain.domain_id,
            description="Identifier of the Amazon OpenSearch Service domain.",
        )
        CfnOutput(
            self,
            "DomainEndpoint",
            value=self.domain.domain_endpoint,
            description="Endpoint of the Amazon OpenSearch Service domain.",
        )
        CfnOutput(
            self,
            "AppLogGroup",
            value=str(self.domain.app_log_group),
            description="Log group that application logs are logged to.",
        )
        CfnOutput(
            self,
            "AuditLogGroup",
            value=str(self.domain.audit_log_group),
            description="Log group that audit logs are logged to.",
        )
        CfnOutput(
            self,
            "SlowIndexLogGroup",
            value=str(self.domain.slow_index_log_group),
            description="Log group that slow indices are logged to.",
        )
        CfnOutput(
            self,
            "SlowSearchLogGroup",
            value=str(self.domain.slow_search_log_group),
            description="Log group that slow searches are logged to.",
        )
