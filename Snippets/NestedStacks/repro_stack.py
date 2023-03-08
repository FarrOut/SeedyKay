from aws_cdk import (core as cdk,
                     aws_ec2 as ec2,
                     )

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class ReproStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        nestedStack = ReproNestedStack(self, 'myNestedStack')


class ReproNestedStack(cdk.NestedStack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        vpc = ec2.Vpc(self, 'myVPC')

        security_group = ec2.SecurityGroup(self, 'sg1',
                                           vpc=vpc,
                                           security_group_name='securityGroupSG1',
                                           )
