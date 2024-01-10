import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { addCodezineScraperFunctionResource } from './resources/codezine-scraper-function-resource';
import { addSummarizeNewsFunctionResource } from './resources/summarize-news-function-resource';
import { addCodezineScraperStateMachineResource } from './resources/codezine-scraper-state-machine-resource';

export class StepFunctionsStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const scraperFunction = addCodezineScraperFunctionResource(this);
        addCodezineScraperStateMachineResource(this, scraperFunction);
        addSummarizeNewsFunctionResource(this);
    }
}