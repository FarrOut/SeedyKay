from aws_cdk import (
    # Duration,
    Stack, aws_ec2 as ec2, aws_wafv2 as wafv2,
    RemovalPolicy, CfnOutput,
)
from constructs import Construct

from motley.components.networking.cloudfront_nestedstack import CloudFrontNestedStack
from motley.components.networking.elb_stack import ElbStack
from motley.components.networking.vpc_stack import VpcNestedStack


class NetworkingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN, waf: wafv2.CfnWebACL = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        net = VpcNestedStack(self, "VpcStack", removal_policy=removal_policy)
        self.vpc = net.vpc

        # elb = ElbStack(self, "ElbStack", vpc=net.vpc, removal_policy=removal_policy)
        web_acl_id = None
        if waf is not None:
            CfnOutput(self, 'WafWebAclArn', value=waf.attr_arn,
                      description='The Amazon Resource Name (ARN) of the web ACL.')
            CfnOutput(self, 'WafWebAclId', value=waf.attr_id,
                      description='The ID of the web ACL.')
            CfnOutput(self, 'WafWebAclName', value=str(waf.name),
                      description='The name of the web ACL.')
            web_acl_id = waf.attr_arn

        cloudfront = CloudFrontNestedStack(self, "CloudFrontNestedStack", web_acl_id=web_acl_id,
                                           removal_policy=removal_policy)
