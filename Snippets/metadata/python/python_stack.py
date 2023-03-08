from aws_cdk import (core as cdk,
aws_ecs as ecs,
)
from aws_cdk.aws_iam import ServicePrincipal, Role, PolicyStatement
# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class PythonStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # L1 Construct
        cluster = ecs.CfnCluster(self, "Cluster")

        cluster.cfn_options.metadata = {
        'resourceMetaKey': 'resourceMetaValue'
        }

        # L2 Construct
        role = Role(self, "MyRole",
                    assumed_by=ServicePrincipal("sns.amazonaws.com")
                    )

        role.add_to_policy(PolicyStatement(
            resources=["*"],
            actions=["lambda:InvokeFunction"]
        ))

        cfn_role = role.node.default_child.add_override(
            'Metadata',
            dict({
                'cfn_nag': {
                    'rules_to_suppress': {
                        'id': "W9",
                        'id': 'W2'
                    }}})
        )
