import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { addCodezineScraperFunctionResource } from './resources/codezine-scaper-function-resource';
import { addSummarizeNewsFunctionResource } from './resources/summarize-news-function-resource';

export class LambdaStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        addCodezineScraperFunctionResource(this);
        addSummarizeNewsFunctionResource(this);
    }
}
