from aws_cdk import (
    # Duration,
    aws_ec2 as ec2,
    aws_iam as iam,
)


class Bootstrapping:

    @staticmethod
    def get_windows_init(instance: ec2.Instance, instance_role: iam.Role, os_type: ec2.OperatingSystemType,
                         user_data: ec2.UserData):
        working_dir = '~/'

        init = ec2.CloudFormationInit.from_config_sets(
            config_sets={
                # Applies the configs below in this order
                "testing": ['test']
            },
            configs={
                'test': ec2.InitConfig([
                    ec2.InitFile.from_string(
                        "c:\cfn\hooks.d\cfn-auto-reloader.conf",
                        "[cfn-auto-reloader-hook]{}".format("\n") +
                        "triggers={}{}".format("post.update", "\n") +
                        "path=Resources.{}.Metadata.AWS::CloudFormation::Init{}".format(instance.instance_id, "\n")
                    ),
                    ec2.InitCommand.shell_command(
                        'touch hello.txt',
                        cwd=working_dir,
                    ),

                ])}
        )
        init.attach(instance.node.default_child, instance_role=instance_role, platform=os_type, user_data=user_data)
        return init
