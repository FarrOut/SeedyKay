import {Stack, StackProps} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import {iCustomBehavior} from "./iCustomBehavior";

export class DistroStack extends Stack {

    private readonly distro: cloudfront.Distribution;

    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        this.distro = new cloudfront.Distribution(this, 'myDist', {
            defaultBehavior: {origin: new origins.HttpOrigin('www.example.com')},
        });
    }

    addAdditionalBehavior(customBehavior: iCustomBehavior): void {
        console.log('Adding additional behavior to CloudFront Distribution: ' + customBehavior.pathPattern)
        this.distro.addBehavior(customBehavior.pathPattern, customBehavior.origin, customBehavior.behaviorOptions)
    }
}
