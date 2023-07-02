from aws_cdk import (
    # Duration,
    Stack,
    aws_codepipeline as codepipeline, aws_kms as kms,
    aws_s3 as s3, aws_codebuild as codebuild, aws_ssm as ssm,aws_iam as iam,
    aws_codecommit as codecommit, aws_codepipeline_actions as codepipeline_actions,
    aws_s3_deployment as s3deploy, RemovalPolicy, CfnOutput, )
from aws_cdk.aws_s3_deployment import BucketDeployment
from constructs import Construct


class CrossAccountCodePipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, remote_account: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        key = kms.Key(self, "MyKey",
                      enable_key_rotation=True,
                      removal_policy=RemovalPolicy.DESTROY,
                      )
        CfnOutput(self, 'KeyArn',
                  description='ARN of this key.',
                  value=key.key_arn,
                  )

        self.param = ssm.StringParameter(self, "Parameter",
                                         allowed_pattern=".*",
                                         description="The ARN of the KMS key to use in cross-account Pipelines.",
                                         parameter_name="KeyArn",
                                         string_value=key.key_arn,
                                         tier=ssm.ParameterTier.STANDARD,
                                         )
        self.param.apply_removal_policy(RemovalPolicy.DESTROY)
        self.param.grant_read(iam.AccountPrincipal(remote_account))

        source_output = codepipeline.Artifact("SourceArtifact")
        bucket = s3.Bucket(self, "MyBucket",
                           removal_policy=RemovalPolicy.DESTROY,
                           auto_delete_objects=True,
                           versioned=True,
                           encryption_key=key,
                           )
        BucketDeployment(self, "DeployAssets",
                         sources=[s3deploy.Source.asset("./motley/CICD/assets")],
                         destination_bucket=bucket,
                         destination_key_prefix="pipeline/"
                         )

        pipeline = codepipeline.Pipeline(self, "MyFirstPipeline",
                                         cross_account_keys=True,
                                         )
        CfnOutput(self, 'PipelineCrossRegionSupport',
                  description='Returns all of the ``CrossRegionSupportStack``s that were generated automatically when '
                              'dealing with Actions that reside in a different region than the Pipeline itself.',
                  value=str(pipeline.cross_region_support),
                  )
        pipeline_arn = str(pipeline.pipeline_arn)
        CfnOutput(self, 'PipelineArn',
                  description='ARN of this pipeline.',
                  value=pipeline_arn,
                  )

        repo = codecommit.Repository(self, "Repository",
                                     repository_name="{}Repository".format(self.stack_name),
                                     description="Repository for {}".format(self.stack_name),
                                     )
        repo.apply_removal_policy(RemovalPolicy.DESTROY)

        source_stage = pipeline.add_stage(
            stage_name="Source",
            actions=[codepipeline_actions.CodeCommitSourceAction(
                action_name="CodeCommit",
                repository=repo,
                output=source_output
            )]
        )

        project = codebuild.PipelineProject(self, "MyProject")
        build_action = codepipeline_actions.CodeBuildAction(
            action_name="CodeBuild",
            project=project,
            input=source_output,
            outputs=[codepipeline.Artifact()],  # optional
            execute_batch_build=True,  # optional, defaults to false
            combine_batch_build_artifacts=True
        )
        build_stage = pipeline.add_stage(
            stage_name="Build",
            actions=[build_action]
        )



