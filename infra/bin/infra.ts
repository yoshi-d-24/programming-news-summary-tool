#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { LambdaStack } from '../lib/lambda/lambda-stack';
import { S3Stack } from '../lib/s3/s3-stack';

const app = new cdk.App();

const env: cdk.Environment = {
  region: 'ap-northeast-1',
}

new LambdaStack(app, 'PNST-LAMBDA', { env, });

new S3Stack(app, 'PNST-S3', { env, });