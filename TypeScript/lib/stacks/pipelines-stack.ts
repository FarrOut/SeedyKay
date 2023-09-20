import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {PipelinesNestedStack} from '../components/cicd/pipelines-nestedstack';

export class PipelinesStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        // let Vpc = new VpcNestedStack(this, 'VpcNestedStack',)

        let Pipe = new PipelinesNestedStack(this, 'PipelinesNestedStack', {
            BranchName: "main", RepositoryOwner: "FarrOut",
            RepositoryName: "SeedyKay",
            StackName: "PipelinesStack",
        })


    }
}
     