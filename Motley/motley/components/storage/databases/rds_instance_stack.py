from aws_cdk import (CfnParameter, aws_ssm as ssm, Fn,
                     Stack, aws_ec2 as ec2, aws_rds as rds, RemovalPolicy, CfnOutput, aws_secretsmanager as secretsmanager, )
from aws_cdk.aws_rds import CfnDBInstance
from constructs import Construct
import json


class RdsInstance(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        instance_type = ec2.InstanceType.of(
            ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL)

        prefix_param = CfnParameter(self, 'RDSInstancePrefix',
                                    )
        db_secret_prefix_param = CfnParameter(self, 'DbSecretPrefix',                                              
                                              )

        parameter_group = rds.ParameterGroup(self, "ParameterGroup",
                                             engine=rds.DatabaseInstanceEngine.postgres(
                                                 version=rds.PostgresEngineVersion.VER_16_1),
                                             description='Testing drift',
                                             parameters={
                                                 "shared_preload_libraries": "pg_stat_statements",
                                                 "track_activity_query_size": "4097"
                                             }
                                             )

        formatted_secret_string_template = json.dumps(
            {"username": f'{prefix_param.value_as_string}_lordcommander'}, indent=4)

        # templated_secret = secretsmanager.Secret(self, "TemplatedSecret",
        #                                          secret_name=f'{
        #                                              db_secret_prefix_param.value_as_string}rds_credentials',
        #                                          generate_secret_string=secretsmanager.SecretStringGenerator(
        #                                              secret_string_template=formatted_secret_string_template,
        #                                              generate_string_key="password",
        #                                              exclude_characters="/@\"",
        #                                              password_length=16
        #                                          )
        #                                          )

        instance = rds.DatabaseInstance(self, "Instance",
                                        engine=rds.DatabaseInstanceEngine.postgres(
                                            version=rds.PostgresEngineVersion.VER_16_2),
                                        # optional, defaults to m5.large
                                        instance_type=instance_type,
                                        allocated_storage=20,
                                        parameter_group=parameter_group,
                                        # Optional - will default to 'admin' username and generated password
                                        # credentials=rds.Credentials.from_generated_secret(
                                        #     "syscdk"),
                                        # credentials=rds.Credentials.from_secret(
                                        #     templated_secret,
                                        # ),
                                        # credentials={
                                        #     "username": templated_secret.secret_value_from_json("username").to_string(),
                                        #     "password": templated_secret.secret_value_from_json("password")
                                        # },
                                        vpc=vpc,
                                        vpc_subnets=ec2.SubnetSelection(
                                            subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                                        ),
                                        removal_policy=removal_policy,
                                        )

        CfnOutput(self, "InstanceEndpoint",
                  value=instance.db_instance_endpoint_address)
        CfnOutput(self, "InstanceIdentifier",
                  value=instance.instance_identifier)
        CfnOutput(self, "InstanceArn", value=instance.instance_arn)

        # ssm.StringParameter(self, "Parameter",
        #                     description=Fn.sub(
        #                         '${RDSInstance} amazonaws.com endpoint',
        #                         variables={
        #                             'RDSInstance': cfn_instance.ref
        #                         }
        #                     ),
        #                     parameter_name=Fn.sub(
        #                         '/DB/${RDSInstance}/DbEndpoint',
        #                         variables={
        #                             'RDSInstance': cfn_instance.ref
        #                         }
        #                     ),
        #                     string_value=str(
        #                         instance.db_instance_endpoint_address),
        #                     tier=ssm.ParameterTier.STANDARD
        #                     )
