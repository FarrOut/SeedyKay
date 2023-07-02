#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import {NetworkingStack} from '../lib/networking/networking-stack';
import {EksStack} from "../lib/orchestration/eks-stack";
import {SecretStack} from "../lib/security/secret-stack";
import {RedshiftStack} from "../lib/storage/redshift-stack";
import {LambdaStack} from "../lib/compute/lambda-stack";
import {ApiGatewayV2Stack} from "../lib/networking/api-gateway-v2-stack";

const app = new cdk.App();

const default_env = {account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION}

const net = new NetworkingStack(app, 'NetworkingStack', {
    env: default_env,
});

new ApiGatewayV2Stack(app, 'ApiGatewayV2Stack', {
    env: default_env,
});

new EksStack(app, 'EksStack', {
    vpc: net.vpc,
    env: default_env,
});

new SecretStack(app, 'SecretStack', {
    env: default_env,
});

let redshift = new RedshiftStack(app, 'RedshiftStack', net.vpc, {
    env: default_env,
});

let lambda = new LambdaStack(app, 'LambdaStack',);