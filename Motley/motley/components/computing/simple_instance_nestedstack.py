from aws_cdk import (
    Duration,
    NestedStack,
    aws_servicediscovery as servicediscovery,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecr as ecr,
    aws_ec2 as ec2,
    CfnOutput,
    Fn,
    RemovalPolicy,
)
from aws_cdk.aws_ecs import ContainerImage, RepositoryImage
from aws_cdk.aws_secretsmanager import ISecret
from aws_cdk.aws_sns import Topic
from constructs import Construct


class SimpleInstanceNestedStack(NestedStack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        security_group: ec2.ISecurityGroup = None,
        key_name: str = None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_data = ec2.UserData.custom("touch ~/hello.txt")        

        instance = ec2.Instance(
            self,
            "MyInstance",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
            ),
            key_name=key_name,
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            security_group=security_group,
            propagate_tags_to_volume_on_creation=True,
            user_data_causes_replacement=True,
            user_data=user_data,
        )
        instance.apply_removal_policy(removal_policy)

        CfnOutput(
            self,
            "InstanceId",
            value=instance.instance_id,
            description="InstanceId of the instance",
        )
        # CfnOutput(self, 'InstancePublicDnsName',
        #           value=str(instance.instance_public_dns_name),
        #           description='Publicly-routable DNS name for this instance.',
        #           )
        CfnOutput(
            self,
            "InstancePrivateDnsName",
            value=str(instance.instance_private_dns_name),
            description="Privately-routable DNS name for this instance.",
        )
        # CfnOutput(self, 'InstancePublicIp',
        #           value=str(instance.instance_public_ip),
        #           description='Public-routable IP address for this instance.',
        #           )
        CfnOutput(
            self,
            "InstancePrivateIp",
            value=str(instance.instance_private_ip),
            description="Private-routable IP address for this instance.",
        )
        CfnOutput(
            self,
            "InstanceAvailabilityZone",
            value=str(instance.instance_availability_zone),
            description="Availability Zone of this instance.",
        )
