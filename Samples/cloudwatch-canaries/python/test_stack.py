from aws_cdk import (core as cdk,
                     aws_synthetics as synthetics,
                     aws_s3 as s3,
                     aws_iam as iam,
                     )

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class TestStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # script_ = 'def handler(event, context): \n' + '   return 200'
        text_file_ = open('canaries\pageLoadBlueprint.py', 'r')
        script_ = text_file_.read()
        text_file_.close()

        bucket_ = s3.Bucket(self, 'myBucket')
        role_ = iam.Role(self, "Role",
                         assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))  # required
        role_.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'))
        role_.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'))

        synth_ = synthetics.CfnCanary(self, 'tweetie',
                                      artifact_s3_location='s3://' + bucket_.bucket_name,
                                      name='tweetiebird',
                                      runtime_version='syn-python-selenium-1.0',
                                      start_canary_after_creation=True,
                                      execution_role_arn=role_.role_arn,
                                      schedule=synthetics.CfnCanary.ScheduleProperty(
                                          expression='rate(1 minute)',
                                      ),
                                      code=synthetics.CfnCanary.CodeProperty(
                                          handler='customer_canary.handler',
                                          script=script_,
                                      ),
                                      #  Workaround for SSL CERTIFICATE_VERIFY_FAILED
                                      # https://moreless.medium.com/how-to-fix-python-ssl-certificate-verify-failed-97772d9dd14c
                                      run_config=synthetics.CfnCanary.RunConfigProperty(
                                          environment_variables={'PYTHONHTTPSVERIFY': '0'},),
                                      )
