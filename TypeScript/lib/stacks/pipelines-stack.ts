import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {LogGroupNestedStack} from "../components/logging/log-group-nestedstack";
import * as logs from 'aws-cdk-lib/aws-logs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import {CodePipeline, CodePipelineSource, ShellStep} from 'aws-cdk-lib/pipelines';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as s3 from 'aws-cdk-lib/aws-s3';
import {S3NestedStack} from "../components/storage/s3-nestedstack";
import {TestingStage, TestType} from "../components/cicd/stages/testing-stage";

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

        this.pipeline = new CodePipeline(this, 'Pipeline', {
            pipelineName: 'MyPipeline',
            selfMutation: true,

            artifactBucket: props.artifactBucket,

            synth: new ShellStep('Synth', {
                input: CodePipelineSource.gitHub(props.RepositoryOwner + '/' + props.RepositoryName, props.BranchName),
                // installCommands: [`cd ${SubDir}`, `pwd`, `ls -la`,
                //     'npm install -g aws-cdk',
                // ],
                commands:
                    [`cd ${props.SubDir}`, `pwd`,
                        'npm ci', `npx cdk --version`,
                        'npm run build',
                        `npx cdk synth ${this.stackName}`],
                primaryOutputDirectory: `${props.SubDir}/cdk.out`,
            }),
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
         * Add testing wave
         *
         */
        const test_account = this.account
        const testingWave = this.pipeline.addWave('Testing')
        testingWave.addStage(new TestingStage(this, 'IntegrationTestingStage',
            {
                testType: TestType.INTEGRATION,
                removalPolicy: props.removalPolicy,
                env: {account: test_account, region: 'eu-west-2'}
            }))
        testingWave.addStage(new TestingStage(this, 'SmokeTestingStage',
            {
                testType: TestType.SMOKE,
                removalPolicy: props.removalPolicy,
                env: {account: test_account, region: 'eu-central-1'}
            }))

    }
}
     