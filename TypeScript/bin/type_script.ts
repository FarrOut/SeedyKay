#!/usr/bin/env node
// import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import {EksStack} from '../lib/stacks/eks-stack';
import {LambdaStack} from '../lib/stacks/lambda-stack';
import {EventsStack} from '../lib/stacks/events-stack';
import {SecurityStack} from '../lib/stacks/security-stack';
import {PipelinesStack} from '../lib/stacks/pipelines-stack';
import * as blueprints from '@aws-quickstart/eks-blueprints';
import {ClusterProvider} from "../lib/blueprints/eks/cluster-provider";
import {networkOverlayAddOns, networkVPCProvider} from "../lib/blueprints/eks/vpc-provider";
import {NetworkingStack} from "../lib/stacks/network-stack";
import {AlbStack} from '../lib/stacks/alb-stack';
import {AutoscalingStack} from '../lib/stacks/autoscaling-stack';
import {IoTStack} from '../lib/stacks/iot-stack';

const app = new cdk.App();

const default_env = {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION
}


let enableAutoscalingStack = false
let enableLambdaStack = false
let enableEksStack = false
let enableBluePrintStack = false
let enableSecurityStack = false
let enablePipelineStack = true
let enableLoadBalancingStack = false
let enableInstanceStack = false
let enableEventsStack = false
let enableLoggingStack = false
let enableIoTStack = false


const net = new NetworkingStack(app, 'CdkTypeScriptNetworkingStack', {
    env: default_env,
});

// if (enableInstanceStack) {
//     new InstanceStack(app, 'InstanceStack', {
//         env: default_env,
//         vpc: net.Vpc,
//         removalPolicy: cdk.RemovalPolicy.DESTROY,
//     });
// }

if (enableAutoscalingStack) {
    new AutoscalingStack(app, 'AutoscalingStack', {
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

if (enableIoTStack) {
    new IoTStack(app, 'IoTStack', {
        env: default_env,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
}

// if (enableLoggingStack) {
//     new LoggingStack(app, 'LoggingStack', {
//         env: default_env,
//         removalPolicy: cdk.RemovalPolicy.DESTROY,
//         retention:logs.RetentionDays.ONE_MONTH,
//     });
// }

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
    new PipelinesStack(app, 'TypeScriptPipelinesStack', {
        env: default_env,

        BranchName: app.node.tryGetContext('BranchName'),
        RepositoryOwner: app.node.tryGetContext('RepositoryOwner'),
        RepositoryName: app.node.tryGetContext('RepositoryName'),
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        SubDir: "TypeScript"
    });
}
