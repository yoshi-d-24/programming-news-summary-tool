import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export const addBucketResource = (scope: Construct): s3.Bucket => {

    const bucket = new s3.Bucket(scope, 'Bucket', {
        bucketName: 'pnst-bucket',
        versioned: false,

        lifecycleRules: [
            {
                id: 'expiration',
                enabled: true,
                expiration: cdk.Duration.days(30),
            },
            {
                id: 'abortIncompleteMultipart',
                enabled: true,
                abortIncompleteMultipartUploadAfter: cdk.Duration.days(1),
            }
        ]

    });

    new cdk.CfnOutput(scope, 'bucketArn', {
        value: bucket.bucketArn,
        exportName: 'PNST-bucketArn'
    });

    return bucket;
}