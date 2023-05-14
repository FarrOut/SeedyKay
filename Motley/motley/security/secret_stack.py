from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2, aws_rds as rds,
    aws_secretsmanager as secretsmanager, RemovalPolicy, )
from aws_cdk.aws_rds import Credentials
from constructs import Construct


class SecretStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        secret = secretsmanager.Secret(
            self,
            "TopSecret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template="{\"username\": \"commander\"}",
                generate_string_key="password",
                password_length=10,
                exclude_characters="':^,()@/",
                exclude_punctuation=True,
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )

        ### How to resolve SecretValue ###
        # secret_value = str(secret.secret_value_from_json("password").unsafe_unwrap())
        #
        # dummy = Topic(self, 'Dummy',
        #               topic_name=secret_value
        #               )
        # CfnOutput(self, 'SecretValue',
        #
        #           description='Resolved secret value',
        #           value=dummy.topic_name
        #           )

        ### Secret Attachment ###
        # Attachable target
        cluster = rds.DatabaseCluster(self, "Database",
                                      engine=rds.DatabaseClusterEngine.aurora_postgres(
                                          version=rds.AuroraPostgresEngineVersion.VER_13_7),
                                      credentials=Credentials.from_secret(secret),
                                      instances=1,
                                      removal_policy=RemovalPolicy.DESTROY,
                                      # Optional - will default to 'admin' username and generated password
                                      instance_props=rds.InstanceProps(
                                          # optional , defaults to t3.medium
                                          instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5,
                                                                            ec2.InstanceSize.LARGE),
                                          vpc_subnets=ec2.SubnetSelection(
                                              subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                                          ),
                                          vpc=vpc
                                      )
                                      )

        new_secret = secretsmanager.Secret(
            self,
            "NewSecret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template="{\"username\": \"commander\"}",
                generate_string_key="password",
                password_length=10,
                exclude_characters="':^,()@/",
                exclude_punctuation=True,
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )

        proxy = rds.DatabaseProxy(self, "Proxy",
                                  proxy_target=rds.ProxyTarget.from_cluster(cluster),
                                  secrets=[new_secret],
                                  vpc=vpc
                                  )

        #
        # CfnOutput(self, 'SecretTargetAttachment',
        #           description='Same as secretArn.',
        #           value=secret_attachment.secret_arn
        #           )
