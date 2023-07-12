from aws_cdk import (
    # Duration,
    NestedStack,
    Stack,
    RemovalPolicy,
    CfnOutput,
    Tags,
    aws_logs as logs,
    aws_wafv2 as wafv2,
)
from constructs import Construct


# Thanks to...
# https://github.com/aws-samples/aws-cdk-examples/tree/master/python/waf


class WafStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        log_group = logs.LogGroup(
            self,
            "LogGroup",
            log_group_name=f"aws-waf-logs-{self.stack_name}",
            # Your log group names must start with aws-waf-logs- and can end with any suffix you like, for example, aws-waf-logs-testLogGroup2.
            # https://docs.aws.amazon.com/waf/latest/developerguide/logging-cw-logs.html#logging-cw-logs-naming
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY,
        )
        CfnOutput(
            self,
            "LogGroupArn",
            description="The ARN of this log group.",
            value=log_group.log_group_arn,
        )
        CfnOutput(
            self,
            "LogGroupName",
            description="The name of this log group.",
            value=log_group.log_group_name,
        )

        # log_stream = logs.LogStream(
        #     self,
        #     "MyLogStream",
        #     log_group=log_group,
        #     # the properties below are optional
        #     # log_stream_name="logStreamName",
        #     removal_policy=RemovalPolicy.DESTROY,
        # )

        # CfnOutput(
        #     self,
        #     "LogStreamName",
        #     description="The name of this log stream.",
        #     value=log_stream.log_stream_name,
        # )

        waf2 = Wafv2Stack(self, "Wafv2Stack")

        # log_group.grant_write(waf2.wafacl)

        logging_configuration = wafv2.CfnLoggingConfiguration(
            self,
            "MyCfnLoggingConfiguration",
            log_destination_configs=[log_group.log_group_arn],
            resource_arn=waf2.wafacl.attr_arn,
            # the properties below are optional
            # logging_filter=logging_filter,
            redacted_fields=[
                {
                    "json_body": {
                        "InvalidFallbackBehavior": "EVALUATE_AS_STRING",
                        "MatchPattern": {
                            "IncludedPaths": ["/path/0/name", "/path/1/name"]
                        },
                        "MatchScope": "ALL",
                    },
                    "method": {},
                    "query_string": {},
                    "single_header": {"Name": "password"},
                    "uri_path": {},
                }
            ],
        )


class Wafv2Stack(NestedStack):
    def make_rules(self, list_of_rules={}):
        rules = list()

        for r in list_of_rules:
            rule = wafv2.CfnWebACL.RuleProperty(
                name=r["name"],
                priority=r["priority"],
                override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
                # override_action={"None": {}},
                statement=wafv2.CfnWebACL.StatementProperty(
                    managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                        name=r["name"], vendor_name="AWS", excluded_rules=[]
                    )  ## managed_rule_group_statement
                ),  ## statement
                visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                    cloud_watch_metrics_enabled=True,
                    metric_name=r["name"],
                    sampled_requests_enabled=True,
                ),  ## visibility_config
            )  ## wafv2.CfnWebACL.RuleProperty
            rules.append(rule)

        #
        # Allowed country list
        #
        ruleGeoMatch = wafv2.CfnWebACL.RuleProperty(
            name="GeoMatch",
            priority=0,
            action=wafv2.CfnWebACL.RuleActionProperty(
                block={}  ## To disable, change to *count*
            ),
            # override_action={"None": {}},
            # override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
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
                metric_name="GeoMatch",
                sampled_requests_enabled=True,
            ),  ## visibility_config
        )  ## GeoMatch
        rules.append(ruleGeoMatch)

        #
        # The rate limit is the maximum number of requests from a
        # single IP address that are allowed in a five-minute period.
        # This value is continually evaluated,
        # and requests will be blocked once this limit is reached.
        # The IP address is automatically unblocked after it falls below the limit.
        #
        ruleLimitRequests100 = wafv2.CfnWebACL.RuleProperty(
            name="LimitRequests100",
            priority=1,
            action=wafv2.CfnWebACL.RuleActionProperty(
                block={}  ## To disable, change to *count*
            ),  ## action
            # override_action={"None": {}},
            # override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
            statement=wafv2.CfnWebACL.StatementProperty(
                rate_based_statement=wafv2.CfnWebACL.RateBasedStatementProperty(
                    limit=100, aggregate_key_type="IP"
                )  ## rate_based_statement
            ),  ## statement
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="LimitRequests100",
                sampled_requests_enabled=True,
            ),
        )  ## limit requests to 100
        rules.append(ruleLimitRequests100)

        return rules

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##
        ## List available Managed Rule Groups using AWS CLI
        ## aws wafv2 list-available-managed-rule-groups --scope REGIONAL
        ##
        managed_rules = [
            {
                "name": "AWSManagedRulesCommonRuleSet",
                "priority": 10,
                "override_action": "none",
                "excluded_rules": [],
            },
            {
                "name": "AWSManagedRulesAmazonIpReputationList",
                "priority": 20,
                "override_action": "none",
                "excluded_rules": [],
            },
            {
                "name": "AWSManagedRulesKnownBadInputsRuleSet",
                "priority": 30,
                "override_action": "none",
                "excluded_rules": [],
            },
            {
                "name": "AWSManagedRulesSQLiRuleSet",
                "priority": 40,
                "override_action": "none",
                "excluded_rules": [],
            },
            {
                "name": "AWSManagedRulesLinuxRuleSet",
                "priority": 50,
                "override_action": "none",
                "excluded_rules": [],
            },
            {
                "name": "AWSManagedRulesUnixRuleSet",
                "priority": 60,
                "override_action": "none",
                "excluded_rules": [],
            },
        ]

        #############################################################
        ##
        ## WAF - Regional, for use in Load Balancers
        ##
        #############################################################
        rulez = self.make_rules(managed_rules)
        print(f"Number of rules: {str(len(rulez))}")

        if not rulez or len(rulez) == 0:
            raise Exception("No rules defined")

        self.wafacl = wafv2.CfnWebACL(
            self,
            id="WAF",
            default_action=wafv2.CfnWebACL.DefaultActionProperty(
                allow=wafv2.CfnWebACL.AllowActionProperty(), block=None
            ),
            ##
            ## The scope of this Web ACL.
            ## Valid options: CLOUDFRONT, REGIONAL.
            ## For CLOUDFRONT, you must create your WAFv2 resources
            ## in the US East (N. Virginia) Region, us-east-1
            ## https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-scope
            ##
            scope="REGIONAL",
            ##
            ## Defines and enables Amazon CloudWatch metrics and web request sample collection.
            ##
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="waf-regional",
                sampled_requests_enabled=True,
            ),
            description="WAFv2 ACL for Regional",
            name="waf-regional",
            rules=rulez,
        )  ## wafv2.CfnWebACL

        Tags.of(self.wafacl).add("Name", "waf-regional", priority=300)
        Tags.of(self.wafacl).add("Purpose", "WAF for Regional", priority=300)
        Tags.of(self.wafacl).add("CreatedBy", "Cloudformation", priority=300)

        CfnOutput(
            self,
            "WafAclArn",
            export_name="WafRegionalStack:WafAclRegionalArn",
            value=self.wafacl.attr_arn,
        )
        CfnOutput(
            self,
            "NumberOfRules",
            value=str(len(rulez)),
        )
