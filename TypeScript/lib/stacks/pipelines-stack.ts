import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {PipelinesNestedStack} from '../components/cicd/pipelines-nestedstack';
import {LogGroupNestedStack} from "../components/logging/log-group-nestedstack";
import * as logs from 'aws-cdk-lib/aws-logs';

export class PipelinesStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        // let Vpc = new VpcNestedStack(this, 'VpcNestedStack',)

        let myRemovalPolicy = cdk.RemovalPolicy.DESTROY;

        let MyLogGroup = new LogGroupNestedStack(this, 'LogGroupNestedStack',
            {removalPolicy: myRemovalPolicy, retention: logs.RetentionDays.ONE_WEEK}).logGroup

        let Pipe = new PipelinesNestedStack(this, 'PipelinesNestedStack', {
            BranchName: "main", RepositoryOwner: "FarrOut",
            RepositoryName: "SeedyKay",
            StackName: "PipelinesStack",
            LogGroup: MyLogGroup,
            removalPolicy: myRemovalPolicy,
        })


    }
}
     