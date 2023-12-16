import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { addNewsTableResource } from './resources/news-table-resource';

export class TableStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        addNewsTableResource(this);
    }
}
