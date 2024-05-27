from aws_cdk import (
    Duration,
    NestedStack, aws_servicediscovery as servicediscovery, aws_elasticloadbalancingv2 as elbv2,
    aws_ecr as ecr, aws_ec2 as ec2, CfnOutput, RemovalPolicy, )
from aws_cdk.aws_ecs import ContainerImage, RepositoryImage
from aws_cdk.aws_secretsmanager import ISecret
from aws_cdk.aws_sns import Topic
from constructs import Construct


class LaunchTemplateNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.IVpc,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 security_group: ec2.ISecurityGroup = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if security_group is None:

            # Define a security group
            security_group = ec2.SecurityGroup(
                self, "SecurityGroup",
                vpc=vpc,
            )

        placement_group = ec2.PlacementGroup(self, "MyPlacementGroup",
                                             spread_level=ec2.PlacementGroupSpreadLevel.HOST,
                                             strategy=ec2.PlacementGroupStrategy.SPREAD,
                                             )
        placement_group.apply_removal_policy(removal_policy)
        CfnOutput(self, "PlacementGroup",
                  value=placement_group.placement_group_name)

        launch_template = ec2.LaunchTemplate(self, "LaunchTemplate",
                                             instance_type=ec2.InstanceType(
                                                 "t2.micro"),
                                             machine_image=ec2.AmazonLinuxImage(),
                                             )
        launch_template.apply_removal_policy(removal_policy)

        CfnOutput(self, "LaunchTemplateName",
                  value=str(launch_template.launch_template_name))
        CfnOutput(self, "LaunchTemplateId",
                  value=str(launch_template.launch_template_id))
