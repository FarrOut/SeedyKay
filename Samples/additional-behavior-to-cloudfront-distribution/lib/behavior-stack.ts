import {RemovalPolicy, Stack, StackProps} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {Bucket, BucketAccessControl} from "aws-cdk-lib/aws-s3";
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import {iCustomBehavior} from "./iCustomBehavior";

export class BehaviorStack extends Stack {
    readonly myCustomBehavior: iCustomBehavior;

    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        const bucket = new Bucket(this, 'Bucket', {
            websiteIndexDocument: 'index.html',
            // publicReadAccess: true,
            accessControl: BucketAccessControl.PRIVATE,
            removalPolicy: RemovalPolicy.DESTROY,
            autoDeleteObjects: true,
        })

        new s3deploy.BucketDeployment(this, 'DeployWebsite', {
            sources: [s3deploy.Source.asset('./website-dist')],
            destinationBucket: bucket,
            destinationKeyPrefix: 'web/static', // optional prefix in destination bucket
        });

        // Export my strange behavior
        this.myCustomBehavior = {
            pathPattern: '/images/*.jpg',
            origin: new origins.S3Origin(bucket),
        }
    }
}
