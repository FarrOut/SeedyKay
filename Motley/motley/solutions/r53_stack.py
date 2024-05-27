from aws_cdk import (
    # Duration,
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
    CfnParameter,
    aws_route53 as r53,
    CfnOutput,
    CfnTag,
    aws_route53profiles as route53profiles,
)
from constructs import Construct
from motley.components.networking.r53_profile_nest import Route53ProfileNest


class Route53Stack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc = None,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Route53ProfileNest(self, 'Route53ProfileNest',
        #                     removal_policy=removal_policy,
        #                     vpc=vpc,
        #                     )

        vpc_id_param = CfnParameter(
            self,
            "VpcId",
            type="AWS::EC2::VPC::Id",
            description="Vpc ID",
        )

        profile = route53profiles.CfnProfile(
            self,
            "MyCfnProfile",
            name="LowProfile",
            # the properties below are optional
            tags=[CfnTag(key="Note", value="hello")],
        )
        profile.apply_removal_policy(removal_policy)

        CfnOutput(
            self,
            "ProfileArn",
            description="The Amazon Resource Name (ARN) of the resolver profile.",
            value=profile.attr_arn,
        )
        CfnOutput(
            self,
            "ProfileId",
            description="The ID of the profile.",
            value=profile.attr_id,
        )

        association = route53profiles.CfnProfileAssociation(
            self,
            "MyCfnProfileAssociation",
            name="VpcAssociation",
            profile_id=profile.attr_id,
            resource_id=vpc.vpc_id,
            tags=[CfnTag(key="Note", value="hello")],
        )

        CfnOutput(
            self,
            "AssociationArn",
            description="The Amazon Resource Name (ARN) of the profile association.",
            value=str(association.arn),
        )
        CfnOutput(
            self,
            "AssociationId",
            description="Primary Identifier for Profile Association.",
            value=str(association.attr_id),
        )
        CfnOutput(
            self,
            "AssociationProfileId",
            description="The ID of the profile that you associated with the resource that is specified by ResourceId.",
            value=str(association.profile_id),
        )
        CfnOutput(
            self,
            "AssociationResourceId",
            description="The resource that you associated the profile with.",
            value=str(association.resource_id),
        )
