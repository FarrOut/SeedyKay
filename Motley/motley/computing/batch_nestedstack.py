from aws_cdk import (
    # Duration,
    NestedStack, aws_efs as efs, aws_batch as batch,
    aws_ec2 as ec2, aws_lambda as lambda_, RemovalPolicy, CfnOutput, )
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy
from aws_cdk.aws_lambda import Runtime, Code
from constructs import Construct

from motley.components.storage.filesystems.efs_nestedstack import EfsNestedStack


class BatchNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 maxv_cpus: int = 256,
                 replace_compute_environment: bool = False,
                 vpc: ec2.IVpc = None,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fargate_compute = batch.FargateComputeEnvironment(
            self,
            "FargateComputeEnv",
            compute_environment_name="FargateEnv",
            vpc=vpc,
            maxv_cpus=maxv_cpus,
            replace_compute_environment=replace_compute_environment,
        )
        fargate_compute.apply_removal_policy(removal_policy)

        CfnOutput(self, "FargateComputeEnvArn",
                  value=fargate_compute.compute_environment_arn,
                  description='The ARN of this compute environment.')

        CfnOutput(self, "FargateComputeEnvName",
                  value=fargate_compute.compute_environment_name,
                  description='The name of this compute environment.')
        CfnOutput(self, "FargateComputeEnvReplaceOnUpdate", value=str(fargate_compute.replace_compute_environment),
                  description='Whether the compute environment should be replaced on update.')
        CfnOutput(self, "FargateComputeMaxvCPUs", value=str(fargate_compute.maxv_cpus),
                  description='The maximum number of vCPUs that an environment can reach.')
