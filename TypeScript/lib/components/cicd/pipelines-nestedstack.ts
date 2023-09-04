import * as eks from 'aws-cdk-lib/aws-eks';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {CodePipeline, CodePipelineSource, ShellStep} from 'aws-cdk-lib/pipelines';

interface PipelinesProps extends cdk.StackProps {
    RepositoryOwner: string,
    RepositoryName: string,
    BranchName: string,
    Vpc?: ec2.IVpc,
}

export class PipelinesNestedStack extends cdk.NestedStack {

    public readonly pipeline: CodePipeline;

    constructor(scope: Construct, id: string, props: PipelinesProps) {
        super(scope, id, props);

        let SubDir = "TypeScript"

        this.pipeline = new CodePipeline(this, 'Pipeline', {
            pipelineName: 'MyPipeline',
            selfMutation: true,

            synth: new ShellStep('Synth', {
                input: CodePipelineSource.gitHub(props.RepositoryOwner + '/' + props.RepositoryName, props.BranchName),
                commands: [`cd ${SubDir}`, `pwd`, 'npm ci', 'npm run build', 'npx cdk synth'],
                primaryOutputDirectory: `${SubDir}/cdk.out`,
            }),
        });
    }

}