import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as lambdaPython from '@aws-cdk/aws-lambda-python-alpha';
import * as path from 'path';
import { Construct } from 'constructs';

export const addCodezineScraperFunctionResource = (scope: Construct): lambdaPython.PythonFunction => {
    // Lambda の実行ロールを作成
    const role = new iam.Role(scope, 'CodezineScraperFunctionRole', {
        roleName: 'PNST-CodezineScraperFunctionRole',
        assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
        managedPolicies: [
            iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
        ],
        inlinePolicies: {
            'INLINE': new iam.PolicyDocument({
                statements: [
                    new iam.PolicyStatement({
                        effect: iam.Effect.ALLOW,
                        actions: [
                            'dynamodb:PutItem',
                            'dynamodb:BatchWriteItem',
                        ],
                        resources: [
                            cdk.Fn.importValue('PNST-newsTableArn'),
                        ],
                    }),
                ]
            })
        }

    });

    return new lambdaPython.PythonFunction(scope, 'CodezineScraperFunction', {
        functionName: 'PNST-CODEZINE-SCRAPER',
        runtime: lambda.Runtime.PYTHON_3_12,
        entry: path.resolve(__dirname, '../../../lambda/codezine_scraper'),
        index: 'index.py',
        handler: 'handler',
        memorySize: 256,
        architecture: lambda.Architecture.ARM_64,
        timeout: cdk.Duration.seconds(60),
        logFormat: lambda.LogFormat.JSON,
        applicationLogLevel: lambda.ApplicationLogLevel.DEBUG,
        role,
    })
}