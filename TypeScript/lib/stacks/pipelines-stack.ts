import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {LogGroupNestedStack} from "../components/logging/log-group-nestedstack";
import * as logs from 'aws-cdk-lib/aws-logs';

interface PipelinesProps extends cdk.StackProps {
    RepositoryOwner: string,
    RepositoryName: string,
    BranchName: string,
    Vpc?: ec2.IVpc,
    LogGroup?: logs.ILogGroup,
    removalPolicy?: cdk.RemovalPolicy,
    SubDir?: string,
}

export class PipelinesStack extends cdk.Stack {

    public readonly pipeline: CodePipeline;

    constructor(scope: Construct, id: string, props: PipelinesProps) {
        super(scope, id, props);

        let MyLogGroup = new LogGroupNestedStack(this, 'LogGroupNestedStack',
            {removalPolicy: myRemovalPolicy, retention: logs.RetentionDays.ONE_WEEK}).logGroup

        this.pipeline = new CodePipeline(this, 'Pipeline', {
            pipelineName: 'MyPipeline',
            selfMutation: true,

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


    }
}
     