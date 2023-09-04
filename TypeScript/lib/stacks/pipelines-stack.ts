import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {VpcNestedStack} from '../components/networking/vpc-nestedstack';
import {EksNestedStack} from '../components/orchestration/eks-nestedstack';
import {KubernetesVersion} from 'aws-cdk-lib/aws-eks';
import {KubectlV24Layer} from '@aws-cdk/lambda-layer-kubectl-v24';
import {PipelinesNestedStack} from '../components/cicd/pipelines-nestedstack';

export class PipelinesStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        let Vpc = new VpcNestedStack(this, 'VpcNestedStack',)

        let Pipe = new PipelinesNestedStack(this, 'PipelinesNestedStack', {
            BranchName: "main", RepositoryOwner: "FarrOut",
            RepositoryName: "SeedyKay"
        })


    }
}
     