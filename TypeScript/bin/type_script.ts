#!/usr/bin/env node
// import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import {EksStack} from '../lib/stacks/eks-stack';
import {LambdaStack} from '../lib/stacks/lambda-stack';
import {SecurityStack} from '../lib/stacks/security-stack';
import {PipelinesStack} from '../lib/stacks/pipelines-stack';
import * as blueprints from '@aws-quickstart/eks-blueprints';
import {ClusterProvider} from "../lib/blueprints/eks/cluster-provider";
import {networkOverlayAddOns, networkVPCProvider} from "../lib/blueprints/eks/vpc-provider";
import {NetworkingStack} from "../lib/stacks/network-stack";

const app = new cdk.App();

const default_env = {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION
}

const net = new NetworkingStack(app, 'NetworkingStack', {
    env: default_env,
});

new LambdaStack(app, 'LambdaStack', {
    env: default_env,
    removalPolicy: cdk.RemovalPolicy.DESTROY,
});

new EksStack(app, 'EksStack', {
    env: default_env,
});


const EksBluePrintStack = blueprints.EksBlueprint.builder()
    .account(process.env.CDK_DEFAULT_ACCOUNT)
    .region(process.env.CDK_DEFAULT_REGION)
    .clusterProvider(ClusterProvider.SAMPLE)
    .addOns(...networkOverlayAddOns)
    .resourceProvider(blueprints.GlobalResources.Vpc, networkVPCProvider)
    .build(app, 'eks-blueprint');

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

