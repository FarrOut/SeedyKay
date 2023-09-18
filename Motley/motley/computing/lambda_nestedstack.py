from aws_cdk import (
    # Duration,
    NestedStack,
    Stack,
    aws_ec2 as ec2,aws_lambda as lambda_,aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2,aws_efs as efs,
    aws_elasticloadbalancingv2_targets as elb_targets,
    aws_autoscaling as autoscaling, CfnOutput, RemovalPolicy, Fn, Tags, )
from constructs import Construct
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy
from aws_cdk.aws_lambda import Runtime, Code
from aws_cdk.aws_efs import FileSystem

class LambdaNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, file_system: FileSystem = None, vpc: ec2.IVpc = None, removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        managed_policy_arn = ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')

        role = Role(self, "Role",
                    assumed_by=ServicePrincipal("lambda.amazonaws.com"),
                    # custom description if desired
                    description="This is a custom role...",
                    managed_policies=[managed_policy_arn],
                    )

        # create a new access point from the filesystem
        access_point = file_system.add_access_point("AccessPoint",
            # set /export/lambda as the root of the access point
            path="/export/lambda",
            # as /export/lambda does not exist in a new efs filesystem, the efs will create the directory with the following createAcl
            create_acl=efs.Acl(
                owner_uid="1001",
                owner_gid="1001",
                permissions="750"
            ),
            # enforce the POSIX identity so lambda function will access with this identity
            posix_user=efs.PosixUser(
                uid="1001",
                gid="1001"
            )
        )


        fn = lambda_.Function(self, "lambda_function",
                              runtime=Runtime.PYTHON_3_9,
                              handler="script.main",
                              role=role,
                              vpc=vpc,
                            #   filesystem=lambda_.FileSystem.from_efs_access_point(access_point, "/mnt/msg"),
                              code=Code.from_asset("./assets/handlers"))