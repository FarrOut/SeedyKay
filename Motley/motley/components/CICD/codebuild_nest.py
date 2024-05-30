from aws_cdk import (
    # Duration,
    NestedStack,
    CfnTag,
    CfnOutput,
    aws_codebuild as codebuild,
    aws_ec2 as ec2,
    Lazy,
    aws_iam as iam,
    RemovalPolicy,
)
from constructs import Construct
from motley.components.CICD.codebuild_updater import CodeBuildUpdater


class CodeBuildNest(NestedStack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        subnet_id: str,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        vpc: ec2.IVpc = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # subnet_id = str(vpc.private_subnets[0].subnet_id)
        subnet_arn = f"arn:aws:ec2:{self.region}:{self.account}:subnet/{subnet_id}"
        # subnet = ec2.Subnet.from_subnet_id(self, "subnet", subnet_id)

        # role = iam.Role(
        #     self,
        #     "CodeBuildRole",
        #     assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
        # )

        # CfnOutput(self, "CodeBuildRoleArn", value=role.role_arn)

        # policy = iam.Policy(
        #     self,
        #     "codebuild-fleet-policy",
        #     statements=[
        #         iam.PolicyStatement(
        #             actions=[
        #                 "ec2:CreateNetworkInterface",
        #                 "ec2:DescribeDhcpOptions",
        #                 "ec2:DescribeNetworkInterfaces",
        #                 "ec2:DeleteNetworkInterface",
        #                 "ec2:DescribeSubnets",
        #                 "ec2:DescribeSecurityGroups",
        #                 "ec2:DescribeVpcs",
        #             ],
        #             effect=iam.Effect.ALLOW,
        #             resources=["*"],
        #         ),
        #         iam.PolicyStatement(
        #             actions=[
        #                 "ec2:CreateNetworkInterfacePermission",
        #                 "ec2:ModifyNetworkInterfaceAttribute",
        #             ],
        #             effect=iam.Effect.ALLOW,
        #             resources=[
        #                 f"arn:aws:ec2:{self.region}:{self.account}:network-interface/*"
        #             ],
        #             conditions={
        #                 # Doesn't work for some reason
        #                 # "StringEquals": {
        #                 #     "ec2:AuthorizedService": "codebuild.amazonaws.com"
        #                 # },
        #                 "ArnEquals": {"ec2:Subnet": [subnet_arn]},
        #             },
        #         ),
        #     ],
        # )
        # policy.attach_to_role(role)

        role = CodeBuildSecurityNest(
            self,
            "CodeBuildSecurityNest",
            subnet_id=subnet_id,
            removal_policy=removal_policy,
        ).role

        fleet = codebuild.CfnFleet(
            self,
            "MyCfnFleet",
            base_capacity=3,
            compute_type="BUILD_GENERAL1_SMALL",
            environment_type="LINUX_CONTAINER",
            tags=[CfnTag(key="Name", value="MyLinuxFleet")],
        )
        fleet.apply_removal_policy(removal_policy)

        # To avoid "Not authorized to perform DescribeSecurityGroups"
        # https://stackoverflow.com/a/60776576
        # fleet.add_depends_on(policy.node.default_child)
        # fleet.add_depends_on(role.node.default_child)
        fleet.add_depends_on(role.node.default_child)

        fleet.add_override("Properties.FleetVpcConfig.VpcId", vpc.vpc_id)
        fleet.add_override(
            "Properties.FleetVpcConfig.Subnets",
            [subnet_id],
        )

        sg = ec2.SecurityGroup(self, "BuildFleetSecurityGroup", vpc=vpc)
        fleet.add_override(
            "Properties.FleetVpcConfig.SecurityGroupIds", [sg.security_group_id]
        )

        fleet.add_override(
            "Properties.FleetServiceRole",
            role.role_arn,
        )

        fleet.add_override("Properties.OverflowBehavior", "QUEUE")

        CfnOutput(self, "FleetId", value=fleet.ref)
        CfnOutput(self, "FleetArn", value=fleet.attr_arn)
        CfnOutput(self, "FleetName", value=str(fleet.name))

        # Update fleet to enable ScalingConfiguration
        params = {
            "arn": fleet.attr_arn,
            "scalingConfiguration": {
                "desiredCapacity": 6,
                "maxCapacity": 12,
                "scalingType": "TARGET_TRACKING_SCALING",
                "targetTrackingScalingConfigs": [
                    {"metricType": "FLEET_UTILIZATION_RATE", "targetValue": 80.0}
                ],
            },
        }

        updater = CodeBuildUpdater(
            self,
            "CodeBuildUpdater",
            parameters=params,
            service_role=role,
        )
        updater.node.add_dependency(fleet)
        # CfnOutput(self, "UpdateResponse", value=str(updater.response))


class CodeBuildSecurityNest(NestedStack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        subnet_id: str,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        vpc: ec2.IVpc = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        subnet_arn = f"arn:aws:ec2:{self.region}:{self.account}:subnet/{subnet_id}"
        CfnOutput(self, "subnet_arn", value=subnet_arn)

        self.role = iam.Role(
            self,
            "CodeBuildRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("codebuild.amazonaws.com"),
                iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
        )
        self.role.apply_removal_policy(removal_policy)

        CfnOutput(self, "CodeBuildRoleArn", value=self.role.role_arn)

        policy = iam.Policy(
            self,
            "codebuild-fleet-policy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "ec2:CreateNetworkInterface",
                        "ec2:DescribeDhcpOptions",
                        "ec2:DescribeNetworkInterfaces",
                        "ec2:DeleteNetworkInterface",
                        "ec2:DescribeSubnets",
                        "ec2:DescribeSecurityGroups",
                        "ec2:DescribeVpcs",
                    ],
                    effect=iam.Effect.ALLOW,
                    resources=["*"],
                ),
                iam.PolicyStatement(
                    actions=[
                        "ec2:CreateNetworkInterfacePermission",
                        "ec2:ModifyNetworkInterfaceAttribute",
                    ],
                    effect=iam.Effect.ALLOW,
                    resources=[
                        f"arn:aws:ec2:{self.region}:{self.account}:network-interface/*"
                    ],
                    conditions={
                        # Doesn't work for some reason
                        # "StringEquals": {
                        #     "ec2:AuthorizedService": "codebuild.amazonaws.com"
                        # },
                        # "ArnEquals": {"ec2:Subnet": [subnet_arn]},
                    },
                ),
            ],
        )
        policy.attach_to_role(self.role)
