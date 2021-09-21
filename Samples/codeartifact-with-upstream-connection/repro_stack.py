# The following example creates a CodeArtifact domain named my-domain to store repositories. It also creates two CodeArtifact repositories: my-repo and my-upstream-repo within the domain. my-repo has my-upstream-repo configured as an upstream repository, and my-upstream-repo has an external connection to the public repository, npmjs.
#
# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeartifact-repository.html#aws-resource-codeartifact-repository--examples

from aws_cdk import (
core as cdk,
aws_codeartifact as codeartifact,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class ReproStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Domain
        domain = codeartifact.CfnDomain(self, 'myDomain',
        domain_name = 'thisismydomain',
        )

        # Upstream repo
        repo = codeartifact.CfnRepository(self, 'myUpstreamRepo',
        repository_name = 'testUpstreamRepo',
        domain_name = domain.domain_name,
        external_connections = ['public:npmjs'],
        )

        # # Primary repository
        # repo = codeartifact.CfnRepository(self, 'myRepo',
        # repository_name = 'testrepo',
        # domain_name = domain.domain_name,
        # upstreams = [upstream_repo.repository_name],
        # )
