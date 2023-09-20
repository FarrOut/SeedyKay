import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {LogGroupNestedStack} from "../components/logging/log-group-nestedstack";
import * as logs from 'aws-cdk-lib/aws-logs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import {CodePipeline, CodePipelineSource, ShellStep, CodeBuildStep, ManualApprovalStep} from 'aws-cdk-lib/pipelines';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as s3 from 'aws-cdk-lib/aws-s3';
import {S3NestedStack} from "../components/storage/s3-nestedstack";
import {MyApplicationStage} from "../components/cicd/stages/my-application-stage";
import {ProductionStage} from "../components/cicd/stages/prod-stage";

interface PipelinesProps extends cdk.StackProps {
    RepositoryOwner: string,
    RepositoryName: string,
    BranchName: string,
    Vpc?: ec2.IVpc,
    LogGroup?: logs.ILogGroup,
    removalPolicy: cdk.RemovalPolicy,
    SubDir?: string,
    artifactBucket?: s3.IBucket,
}

export class PipelinesStack extends cdk.Stack {

    public readonly pipeline: CodePipeline;

    constructor(scope: Construct, id: string, props: PipelinesProps) {
        super(scope, id, props);

        props.LogGroup = new LogGroupNestedStack(this, 'LogGroupNestedStack',
            {removalPolicy: props.removalPolicy, retention: logs.RetentionDays.ONE_WEEK}).logGroup

        props.artifactBucket = new S3NestedStack(this, 'ArtifactBucketNestedStack', {
            removalPolicy: props.removalPolicy,
            autoDeleteObjects: true,
            bucketName: cdk.PhysicalName.GENERATE_IF_NEEDED,
        }).bucket

        const synthStep = new ShellStep('Synth', {
            input: CodePipelineSource.gitHub(props.RepositoryOwner + '/' + props.RepositoryName, props.BranchName),
            // installCommands: [`cd ${SubDir}`, `pwd`, `ls -la`,
            //     'npm install -g aws-cdk',
            // ],
            commands:
                [`cd ${props.SubDir}`, `pwd`,
                    'npm ci', `npx cdk --version`,
                    'npm run build',
                    `npx cdk synth ${this.stackName}`],
            /*
             * We need to define 'primaryOutputDirectory' because
             * our CDK app is not in the root of the project structure.
             */
            primaryOutputDirectory: `${props.SubDir}/cdk.out`,
        })

        this.pipeline = new CodePipeline(this, 'Pipeline', {
            pipelineName: 'MyPipeline',
            selfMutation: true,

            artifactBucket: props.artifactBucket,

            synth: synthStep,
            codeBuildDefaults: {
                buildEnvironment: {
                    // privileged: true,
                    // buildImage: codebuild.LinuxBuildImage.STANDARD_6_0,
                    // computeType: codebuild.ComputeType.MEDIUM,
                },
                partialBuildSpec: codebuild.BuildSpec.fromObject({
                    env: {
                        variables: {
                            // CDK env variables propagation
                            GIT_BRANCH: props.BranchName,
                            // NODE_VERSION: '16',
                        },
                    },
                }),
                logging: {
                    cloudWatch: {
                        logGroup: props.LogGroup,
                    }
                },
            },
        });

        /**
         *
         * Add Testing wave
         *
         */
        const testingWave = this.pipeline.addWave('Testing')
        testingWave.addStage(new MyApplicationStage(this, 'TestingStageAlpha',
            {
                removalPolicy: props.removalPolicy,
            })).addPost(
            new CodeBuildStep('RunIntegrationTests', {
                input: synthStep,
                installCommands: [
                    'npm run install-all',
                    'sudo apt-get install jq'
                ],
                commands: [
                    'echo "Let\'s run some tests!!"',
                ],
                env: {},
                primaryOutputDirectory: `${props.SubDir}/cdk.out`,
            }),
        )
        testingWave.addStage(new MyApplicationStage(this, 'TestingStageBeta',
            {
                removalPolicy: props.removalPolicy,
            }))
        testingWave.addStage(new MyApplicationStage(this, 'TestingStageGamma',
            {
                removalPolicy: props.removalPolicy,
            }))

        /**
         *
         * Add Release wave
         *
         */
        const releaseWave = this.pipeline.addWave('Release')
        releaseWave.addStage(
            new MyApplicationStage(this, 'ProductionStage',
                {
                    removalPolicy: props.removalPolicy,
                }),
            {
                pre: [
                    // new ManualApprovalStep('PromoteToProd'),
                ],
            }
        )
    }
}
     