#!/usr/bin/env node
// import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import {EksStack} from '../lib/stacks/eks-stack';
import {LambdaStack} from '../lib/stacks/lambda-stack';
import {SecurityStack} from '../lib/stacks/security-stack';
import {PipelinesStack} from '../lib/stacks/pipelines-stack';

const app = new cdk.App();

const default_env = {account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION}

// const net = new NetworkingStack(app, 'NetworkingStack', {
//     env: default_env,
// });

new LambdaStack(app, 'LambdaStack', {
    env: default_env,
    removalPolicy: cdk.RemovalPolicy.DESTROY,
});

new EksStack(app, 'EksStack', {
    env: default_env,
});

new SecurityStack(app, 'SecurityStack', {
    env: default_env,
});

new PipelinesStack(app, 'PipelinesStack', {
    env: default_env,

    BranchName: "main",
    RepositoryOwner: "FarrOut",
    RepositoryName: "SeedyKay",
    removalPolicy: cdk.RemovalPolicy.DESTROY,
    SubDir: "TypeScript"
});

