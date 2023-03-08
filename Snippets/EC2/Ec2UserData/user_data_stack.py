from aws_cdk import (core as cdk,
                     aws_ec2 as ec2,
                     )

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

# Replication of Blue/Green deployment with AWS Developer tools on Amazon EC2 using Amazon EFS to host application source code
# https://aws.amazon.com/blogs/devops/integrating-sonarqube-as-a-pull-request-approver-on-aws-codecommit/

# SonarQube
# https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-9.0.1.46107.zip


class UserDataStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_ = ec2.Vpc(self, 'myVPC')

        # SonarQube instance setup
        sonarqube = ec2.Instance(self, 'SonarQube',
                                 vpc=vpc_,
                                 instance_type=ec2.InstanceType.of(
                                     ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
                                 key_name='myKey',
                                 machine_image=ec2.MachineImage.latest_amazon_linux(),
                                 )

        nl = '\n'
        user_data_ = 'sudo yum update' + nl + \
            'sudo yum install java-11-amazon-corretto-headless wget' + nl + \
            'cd ~/' + nl + \
            'wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-9.0.1.46107.zip' + nl

        sonarqube.add_user_data(ec2.UserData.custom(user_data_).render())
