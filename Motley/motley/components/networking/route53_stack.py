from aws_cdk import (
    # Duration,
    Stack, aws_route53 as route53,
    aws_ec2 as ec2, CfnOutput, RemovalPolicy, NestedStack, )
from aws_cdk.aws_route53 import HostedZone, CfnRecordSetGroup
from constructs import Construct


class Route53Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, zone_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.domain_stack = DomainStack(self, "DomainStack",
                                        zone_name=zone_name,
                                        vpc=vpc,
                                        )

        self.recordset_stack = RecordSetStack(self, "RecordSetStack",
                                              hosted_zone=self.domain_stack.zone,
                                              )


class DomainStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, zone_name: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.zone = route53.HostedZone(self, "HostedZone",
                                       zone_name=zone_name,
                                       vpcs=[vpc],
                                       )
        self.zone.apply_removal_policy(RemovalPolicy.DESTROY)

        CfnOutput(self, 'HostedZoneArn',
                  description='ARN of this hosted zone',
                  value=str(self.zone.hosted_zone_arn),
                  )

        CfnOutput(self, 'HostedZoneId',
                  description='ID of this hosted zone, such as “Z23ABC4XYZL05B”.',
                  value=str(self.zone.hosted_zone_id),
                  )

        CfnOutput(self, 'HostedZoneName',
                  description='FQDN of this hosted zone.',
                  value=str(self.zone.zone_name),
                  )


class RecordSetStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, hosted_zone: HostedZone, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        record_set_one = CfnRecordSetGroup.RecordSetProperty(
            name="test.{}".format(hosted_zone.zone_name),
            type="CNAME",
        )

        record_set_two = CfnRecordSetGroup.RecordSetProperty(
            name="sandbox.{}".format(hosted_zone.zone_name),
            type="CNAME",
        )

        record_set_group = CfnRecordSetGroup(self, "MyCfnRecordSetGroup",
                                             comment='My group of RecordSets',
                                             hosted_zone_id=hosted_zone.hosted_zone_id,
                                             record_sets=[
                                                 record_set_one, record_set_two],
                                             )
        CfnOutput(self, 'RecordSetGroupName',
                  description='The name of the record set group,',
                  value=str(record_set_group.ref),
                  )
