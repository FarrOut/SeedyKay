from aws_cdk import (core as cdk,
aws_codebuild as cb,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class ReproStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        buildspec = cb.BuildSpec.from_object_to_yaml({
            'version': 0.2,
            'phases': {
                'build': {
                    'commands': [
                        'echo "Hello, CodeBuild!"',
                    ],
                },
            },
        })
        print('Buildspec:\n' + buildspec.to_build_spec() )

        project = cb.Project(self, 'BobTheBuilder',
        build_spec = buildspec,
        )
