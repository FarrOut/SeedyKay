import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {CodePipeline, CodePipelineSource, ShellStep} from 'aws-cdk-lib/pipelines';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as iam from 'aws-cdk-lib/aws-iam';

interface PipelinesProps extends cdk.StackProps {
    RepositoryOwner: string,
    RepositoryName: string,
    BranchName: string,
    Vpc?: ec2.IVpc,
    StackName: string,
    LogGroup?: logs.ILogGroup,
    removalPolicy?: cdk.RemovalPolicy,
    stackName?: string,
}

export class PipelinesNestedStack extends cdk.NestedStack {

    public readonly pipeline: CodePipeline;

    // rolePolicyStatements: [
    //     new iam.PolicyStatement({
    //         actions: ['sts:AssumeRole'],
    //         resources: ['*'],
    //         conditions: {
    //             StringEquals: {
    //                 'iam:ResourceTag/aws-cdk:bootstrap-role':
    //                     `arn:aws:iam::${AWS::AccountId}:role/cdk-${Qualifier}-lookup-role-${AWS::AccountId}-${AWS::Region}`,
    //             },
    //         },
    //     }),
    // ],


    constructor(scope: Construct, id: string, props: PipelinesProps) {
        super(scope, id, props);

        let SubDir = "TypeScript"

        this.pipeline = new CodePipeline(this, 'Pipeline', {
            pipelineName: 'MyPipeline',
            selfMutation: true,

            synth: new ShellStep('Synth', {
                input: CodePipelineSource.gitHub(props.RepositoryOwner + '/' + props.RepositoryName, props.BranchName),
                // installCommands: [`cd ${SubDir}`, `pwd`, `ls -la`,
                //     'npm install -g aws-cdk',
                // ],
                commands:
                    [`cd ${SubDir}`, `pwd`,
                        'npm ci', `npx cdk --version`,
                        'npm run build',
                        `npx cdk synth ${props.StackName}`],
                primaryOutputDirectory: `${SubDir}/cdk.out`,
            }),
            codeBuildDefaults: {
                buildEnvironment: {
                    // privileged: true,
                    // buildImage: codebuild.LinuxBuildImage.STANDARD_6_0,
                    // computeType: codebuild.ComputeType.MEDIUM,
                },
                partialBuildSpec: codebuild.BuildSpec.fromObject({
                    phases: {
                        // "install": {
                        //     "commands": [
                        //         "npm install -g aws-cdk@2"
                        //     ]
                        // },
                        build: {
                            commands: [
                                `cdk -a . deploy ${props.stackName} --require-approval=never --verbose`
                            ]
                        }
                    },
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