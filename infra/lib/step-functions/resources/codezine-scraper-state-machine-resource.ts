import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambdaPython from '@aws-cdk/aws-lambda-python-alpha';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';
import { Construct } from 'constructs';

export const addCodezineScraperStateMachineResource = (scope: Construct): stepfunctions.StateMachine => {

    const role = new iam.Role(scope, 'CodezineScraperStateMachineRole', {
        roleName: 'PNST-CodezineScraperStateMachineRole',
        assumedBy: new iam.ServicePrincipal(
            `states.${cdk.Aws.REGION}.amazonaws.com`
        ),
        inlinePolicies: {
            'INLINE': new iam.PolicyDocument({
                statements: [
                    new iam.PolicyStatement({
                        effect: iam.Effect.ALLOW,
                        actions: [
                            'lambda:InvokeFunction',
                        ],
                        resources: [
                            `arn:aws:lambda:${cdk.Aws.REGION}:${cdk.Aws.ACCOUNT_ID}:function:PNST-CODEZINE-SCRAPER:*`,
                        ],
                    }),
                ]
            })
        }
    });

    const scraperFunction = getCodezineScraperFunctionResource(scope);

    const scraperTask = new tasks.LambdaInvoke(scope, 'ScraperTask', {
        lambdaFunction: scraperFunction,
        outputPath: '$.Payload',
    });

    const succeed = new stepfunctions.Succeed(scope, 'ScraperSucceed', {
        stateName: 'succeeded'
    });

    const definition = scraperTask
        .next(succeed);

    const stateMachine = new stepfunctions.StateMachine(scope, 'CodezineScraperStateMachine', {
        stateMachineName: 'PNST-CODEZINE-SCRAPER',
        role,
        definitionBody: stepfunctions.DefinitionBody.fromChainable(definition),
    });

    new events.Rule(scope, 'ScraperRule', {
        ruleName: 'PNST-CODEZINE-SCRAPER-EXECUTE',
        schedule: events.Schedule.cron({ minute: '0', hour: '0' }),
        targets: [
            new targets.SfnStateMachine(stateMachine),
        ],
    });

    return stateMachine;
}

const getCodezineScraperFunctionResource = (scope: Construct): lambdaPython.PythonFunction => {
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
                            's3:PutObject',
                        ],
                        resources: [
                            `${cdk.Fn.importValue('PNST-bucketArn')}/*`,
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
        memorySize: 512,
        architecture: lambda.Architecture.ARM_64,
        timeout: cdk.Duration.minutes(10),
        logFormat: lambda.LogFormat.JSON,
        applicationLogLevel: lambda.ApplicationLogLevel.INFO,
        role,
    })
}