import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cdk from 'aws-cdk-lib';
import {Construct} from 'constructs';

interface MyStackProps extends cdk.StackProps {
    removalPolicy: cdk.RemovalPolicy,
    autoDeleteObjects: boolean,
    bucketName?: string,
}

export class S3NestedStack extends cdk.NestedStack {

    public readonly bucket: s3.IBucket;

    constructor(scope: Construct, id: string, props: MyStackProps) {
        super(scope, id, props);

        this.bucket = new s3.Bucket(scope, 'Bucket', {
            bucketName: props.bucketName,

            blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
            encryption: s3.BucketEncryption.S3_MANAGED,
            enforceSSL: true,
            versioned: true,
            removalPolicy: props.removalPolicy,
            autoDeleteObjects: props.autoDeleteObjects,
        });

        new cdk.CfnOutput(this, 'BucketArn', {
            value: this.bucket.bucketArn,
            description: 'The ARN of the bucket.', // Optional
        });
        new cdk.CfnOutput(this, 'BucketDomainName', {
            value: this.bucket.bucketDomainName,
            description: 'The IPv4 DNS name of the specified bucket.', // Optional
        });
        new cdk.CfnOutput(this, 'BucketName', {
            value: this.bucket.bucketName,
            description: 'The name of the bucket.', // Optional
        });
        new cdk.CfnOutput(this, 'IsWebsite', {
            value: String(this.bucket.isWebsite),
            description: 'If this bucket has been configured for static website hosting.', // Optional
        });
        new cdk.CfnOutput(this, 'BucketWebsiteUrl', {
            value: this.bucket.bucketWebsiteUrl,
            description: 'The URL of the static website.', // Optional
        });
    }
}