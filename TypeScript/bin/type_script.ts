#!/usr/bin/env node
// import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { EksStack } from '../lib/stacks/eks-stack';
import { LambdaStack } from '../lib/stacks/lambda-stack';
import { EventsStack } from '../lib/stacks/events-stack';
import { SecurityStack } from '../lib/stacks/security-stack';
import { PipelinesStack } from '../lib/stacks/pipelines-stack';
import * as blueprints from '@aws-quickstart/eks-blueprints';
import { ClusterProvider } from "../lib/blueprints/eks/cluster-provider";
import { networkOverlayAddOns, networkVPCProvider } from "../lib/blueprints/eks/vpc-provider";
import { NetworkingStack } from "../lib/stacks/network-stack";
import { AlbStack } from '../lib/stacks/alb-stack';
import {InstanceStack} from "../lib/stacks/instance-stack";

const app = new cdk.App();

const default_env = {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION
}


let enableLambdaStack = false
let enableEksStack = false
let enableBluePrintStack = false
let enableSecurityStack = false
let enablePipelineStack = false
let enableLoadBalancingStack = false
let enableInstanceStack = false
let enableEventsStack = true

const net = new NetworkingStack(app, 'CdkTypeScriptNetworkingStack', {
    env: default_env,
});

if (enableInstanceStack) {
    new InstanceStack(app, 'InstanceStack', {
        env: default_env,
        vpc: net.Vpc,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
}

if (enableLambdaStack) {
    new LambdaStack(app, 'LambdaStack', {
        env: default_env,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
}

if (enableEventsStack) {
    new EventsStack(app, 'EventsStack', {
        env: default_env,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        PrincipalOrgID: app.node.tryGetContext('PrincipalOrgID'),
    });
}


if (enableLoadBalancingStack) {
    new AlbStack(app, 'AlbStack', {
        env: default_env,
        vpc: net.Vpc,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
}

if (enableEksStack) {
    new EksStack(app, 'EksStack', {
        env: default_env,
    });
}

if (enableBluePrintStack) {
    const EksBluePrintStack = blueprints.EksBlueprint.builder()
        .account(process.env.CDK_DEFAULT_ACCOUNT)
        .region(process.env.CDK_DEFAULT_REGION)
        .clusterProvider(ClusterProvider.SAMPLE)
        .addOns(...networkOverlayAddOns)
        .resourceProvider(blueprints.GlobalResources.Vpc, networkVPCProvider)
        .build(app, 'eks-blueprint');
}

if (enableSecurityStack) {
    new SecurityStack(app, 'SecurityStack', {
        env: default_env,
    });
}

if (enablePipelineStack) {
    new PipelinesStack(app, 'PipelinesStack', {
        env: default_env,

        BranchName: "main",
        RepositoryOwner: "FarrOut",
        RepositoryName: "SeedyKay",
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        SubDir: "TypeScript"
    });
}
