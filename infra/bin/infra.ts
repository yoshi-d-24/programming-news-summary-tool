#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { TableStack } from '../lib/dynamo-db/table-stack';
import { LambdaStack } from '../lib/lambda/lambda-stack';

const app = new cdk.App();

const env: cdk.Environment = {
  region: 'ap-northeast-1',
}

new TableStack(app, 'PNST-TABLE', { env, });

new LambdaStack(app, 'PNST-LAMBDA', { env, });