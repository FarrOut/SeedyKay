from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_wafv2 as wafv2,
    CfnOutput,
    RemovalPolicy, Tags,
)
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_logs import LogGroup, RetentionDays
from constructs import Construct


def make_rules(list_of_rules={}):
    rules = list()
    for r in list_of_rules:
        rule = wafv2.CfnWebACL.RuleProperty(
            name=r["name"],
            priority=r["priority"],
            override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
            statement=wafv2.CfnWebACL.StatementProperty(
                managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                    name=r["name"],
                    vendor_name="AWS",
                    excluded_rules=[]
                )  ## managed_rule_group_statement
            ),  ## statement
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name=r["name"],
                sampled_requests_enabled=True
            )  ## visibility_config
        )  ## wafv2.CfnWebACL.RuleProperty
        rules.append(rule)

    ##
    ## Allowed country list
    ##
    ruleGeoMatch = wafv2.CfnWebACL.RuleProperty(
        name='GeoMatch',
        priority=0,
        action=wafv2.CfnWebACL.RuleActionProperty(
            block={}  ## To disable, change to *count*
        ),
        statement=wafv2.CfnWebACL.StatementProperty(
            not_statement=wafv2.CfnWebACL.NotStatementProperty(
                statement=wafv2.CfnWebACL.StatementProperty(
                    geo_match_statement=wafv2.CfnWebACL.GeoMatchStatementProperty(
                        ##
                        ## block connection if source not in the below country list
                        ##
                        country_codes=[
                            "AR",  ## Argentina
                            "BO",  ## Bolivia
                            "BR",  ## Brazil
                            "CL",  ## Chile
                            "CO",  ## Colombia
                            "EC",  ## Ecuador
                            "FK",  ## Falkland Islands
                            "GF",  ## French Guiana
                            "GY",  ## Guiana
                            "GY",  ## Guyana
                            "PY",  ## Paraguay
                            "PE",  ## Peru
                            "SR",  ## Suriname
                            "UY",  ## Uruguay
                            "VE",  ## Venezuela
                        ]  ## country_codes
                    )  ## geo_match_statement
                )  ## statement
            )  ## not_statement
        ),  ## statement
        visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
            cloud_watch_metrics_enabled=True,
            metric_name='GeoMatch',
            sampled_requests_enabled=True
        )  ## visibility_config
    )  ## GeoMatch
    rules.append(ruleGeoMatch)

    ##
    ## The rate limit is the maximum number of requests from a
    ## single IP address that are allowed in a five-minute period.
    ## This value is continually evaluated,
    ## and requests will be blocked once this limit is reached.
    ## The IP address is automatically unblocked after it falls below the limit.
    ##
    ruleLimitRequests100 = wafv2.CfnWebACL.RuleProperty(
        name='LimitRequests100',
        priority=1,
        action=wafv2.CfnWebACL.RuleActionProperty(
            block={}  ## To disable, change to *count*
        ),  ## action
        statement=wafv2.CfnWebACL.StatementProperty(
            rate_based_statement=wafv2.CfnWebACL.RateBasedStatementProperty(
                limit=100,
                aggregate_key_type="IP"
            )  ## rate_based_statement
        ),  ## statement
        visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
            cloud_watch_metrics_enabled=True,
            metric_name='LimitRequests100',
            sampled_requests_enabled=True
        )
    )  ## limit requests to 100
    rules.append(ruleLimitRequests100);

    return rules


class WafCloudFrontStack(Stack):

    def __init__(
            self, scope: Construct, construct_id: str,
            removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##
        ## List available Managed Rule Groups using AWS CLI
        ## aws wafv2 list-available-managed-rule-groups --scope CLOUDFRONT
        ##
        managed_rules = [{
            "name": "AWSManagedRulesCommonRuleSet",
            "priority": 10,
            "override_action": "none",
            "excluded_rules": [],
        }, {
            "name": "AWSManagedRulesAmazonIpReputationList",
            "priority": 20,
            "override_action": "none",
            "excluded_rules": [],
        }, {
            "name": "AWSManagedRulesKnownBadInputsRuleSet",
            "priority": 30,
            "override_action": "none",
            "excluded_rules": [],
        }, {
            "name": "AWSManagedRulesSQLiRuleSet",
            "priority": 40,
            "override_action": "none",
            "excluded_rules": [],
        }, {
            "name": "AWSManagedRulesLinuxRuleSet",
            "priority": 50,
            "override_action": "none",
            "excluded_rules": [],
        }, {
            "name": "AWSManagedRulesUnixRuleSet",
            "priority": 60,
            "override_action": "none",
            "excluded_rules": [],
        }]

        self.waf = wafv2.CfnWebACL(self, 'WebACL',
                                   default_action=wafv2.CfnWebACL.DefaultActionProperty(
                                       allow=wafv2.CfnWebACL.AllowActionProperty(), block=None),
                                   ##
                                   ## The scope of this Web ACL.
                                   ## Valid options: CLOUDFRONT, REGIONAL.
                                   ## For CLOUDFRONT, you must create your WAFv2 resources
                                   ## in the US East (N. Virginia) Region, us-east-1
                                   ## https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-scope
                                   ##
                                   scope="CLOUDFRONT",

                                   ##
                                   ## Defines and enables Amazon CloudWatch metrics and web request sample collection.
                                   ##
                                   visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                                       cloud_watch_metrics_enabled=True,
                                       metric_name="waf-cloudfront",
                                       sampled_requests_enabled=True
                                   ),
                                   description="WAFv2 ACL for CloudFront",
                                   # name="waf-cloudfront",
                                   rules=make_rules(managed_rules),
                                   )
        self.waf.apply_removal_policy(removal_policy)

        Tags.of(self.waf).add("Name", "waf-cloudfront", priority=300)
        Tags.of(self.waf).add("Purpose", "WAF for CloudFront", priority=300)
        Tags.of(self.waf).add("CreatedBy", "Cloudformation", priority=300)

        CfnOutput(self, 'WafWebAclArn', value=self.waf.attr_arn,
                  description='The Amazon Resource Name (ARN) of the web ACL.')
        CfnOutput(self, 'WafWebAclId', value=self.waf.attr_id,
                  description='The ID of the web ACL.')
        CfnOutput(self, 'WafWebAclName', value=str(self.waf.name),
                  description='The name of the web ACL.')
