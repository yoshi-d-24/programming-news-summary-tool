import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { addNewsTableResource } from './resources/news-table-resource';

export class TableStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const table = addNewsTableResource(this);

        new cdk.CfnOutput(this, 'newsTableArnOutPut', {
            value: table.tableArn,
            exportName: 'PNST-newsTableArn',
        });
    }
}
