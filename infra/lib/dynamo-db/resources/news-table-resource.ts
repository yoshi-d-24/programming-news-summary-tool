import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

export const addNewsTableResource = (scope: Construct): dynamodb.TableV2 => {
    const table = new dynamodb.TableV2(scope, 'NewsTable', {
        tableName: 'PNST-NEWS',
        billing: dynamodb.Billing.onDemand(),
        partitionKey: {
            name: 'code',
            type: dynamodb.AttributeType.STRING,
        },
        sortKey: {
            name: 'id',
            type: dynamodb.AttributeType.NUMBER,
        },
        localSecondaryIndexes: [
            {
                indexName: 'date',
                sortKey: {
                    name: 'date',
                    type: dynamodb.AttributeType.NUMBER,
                }
            }
        ],
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