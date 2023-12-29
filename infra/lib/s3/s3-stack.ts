import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { addBucketResource } from './resources/bucket-resource';

export class S3Stack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        addBucketResource(this);
    }
}
