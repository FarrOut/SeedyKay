#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import {BehaviorStack} from '../lib/behavior-stack';
import {DistroStack} from "../lib/distro-stack";
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';

const app = new cdk.App();

const b_stack = new BehaviorStack(app, 'BehaviorStack', {
    env: {account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION},
});

const d_stack = new DistroStack(app, 'DistroStack', {
    env: {account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION},
});

// Pass my custom behavior from Stack B to the CloudFront Distribution in Stack D...
d_stack.addAdditionalBehavior(b_stack.myCustomBehavior)

// Add a second ad hoc behavior...
d_stack.addAdditionalBehavior({
    pathPattern: '/videos/*.mp4',
    origin: new origins.HttpOrigin('www.blahblah.com')
})
