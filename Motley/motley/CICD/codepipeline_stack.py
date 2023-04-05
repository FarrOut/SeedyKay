from aws_cdk import (
    # Duration,
    Stack,
    aws_codepipeline as codepipeline,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy, RemovalPolicy,
)
from aws_cdk.aws_codepipeline import StageProps
from aws_cdk.aws_codepipeline_actions import CloudFormationDeployStackSetAction, StackSetTemplate, \
    StackSetDeploymentModel, StackInstances, \
    S3SourceAction, S3Trigger
from aws_cdk.aws_s3_deployment import BucketDeployment
from constructs import Construct


class CodePipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_output = codepipeline.Artifact("SourceArtifact")
        bucket = s3.Bucket(self, "MyBucket",
                           removal_policy=RemovalPolicy.DESTROY,
                           auto_delete_objects=True,
                           versioned=True,
                           )
        BucketDeployment(self, "DeployAssets",
                         sources=[s3deploy.Source.asset("./assets")],
                         destination_bucket=bucket,
                         destination_key_prefix="pipeline/"
                         )

        pipeline = codepipeline.Pipeline(self, "MyFirstPipeline",
                                         stages=[StageProps(
                                             stage_name="stageName",

                                             # the properties below are optional
                                             actions=[S3SourceAction(
                                                 action_name="S3Source",
                                                 bucket_key="pipeline/template.yaml",
                                                 bucket=bucket,
                                                 output=source_output,
                                                 trigger=S3Trigger.EVENTS
                                             )],
                                             transition_disabled_reason="transitionDisabledReason",
                                             transition_to_enabled=False
                                         )],
                                         )

        stackset_stage = pipeline.add_stage(
            stage_name="DeployStackSets",
            actions=[
                # First, update the StackSet itself with the newest template
                CloudFormationDeployStackSetAction(
                    action_name="UpdateStackSet",
                    run_order=1,
                    stack_set_name="PipelineStackSet",
                    template=StackSetTemplate.from_artifact_path(
                        source_output.at_path("template.yaml")),

                    # Change this to 'StackSetDeploymentModel.organizations()' if you want to deploy to OUs
                    deployment_model=StackSetDeploymentModel.self_managed(),
                    # This deploys to a set of accounts
                    stack_instances=StackInstances.in_accounts([self.account],
                                                               [self.region])
                ),

            ]
        )
