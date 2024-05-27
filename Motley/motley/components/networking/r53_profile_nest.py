from aws_cdk import (
    # Duration,
    NestedStack,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3 as s3,
    aws_route53 as r53,
    aws_route53profiles as route53profiles,
    aws_s3_deployment as s3deploy,
    aws_apigateway as apigateway,
    RemovalPolicy,
    CfnTag,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ec2 as ec2,
    CfnOutput,
    CfnOutput,
)
from constructs import Construct


class Route53ProfileNest(NestedStack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

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
