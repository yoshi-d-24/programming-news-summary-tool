import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

export const addNewsTableResource = (scope: Construct): dynamodb.TableV2 => {
    const table = new dynamodb.TableV2(scope, 'NewsTable', {
        tableName: 'PNST-NEWS',
        partitionKey: {
            name: 'id',
            type: dynamodb.AttributeType.STRING,
        },
        billing: dynamodb.Billing.onDemand(),
        timeToLiveAttribute: 'ttl',
        tags: [
            {
                key: 'NAME',
                value: 'PNST-NEWS',
            },
        ],
    });

    return table;
}