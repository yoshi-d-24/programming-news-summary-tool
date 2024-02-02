import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { addCodezineScraperStateMachineResource } from './resources/codezine-scraper-state-machine-resource';
import { addSummarizeNewsStateMachineResource } from './resources/summarize-news-state-machine-resource';
import { addGenerateMarkdownStateMachineResource } from './resources/generate_markdown-state-machine-resource';

export class StepFunctionsStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        addCodezineScraperStateMachineResource(this);
        addSummarizeNewsStateMachineResource(this);
        addGenerateMarkdownStateMachineResource(this);
    }
}