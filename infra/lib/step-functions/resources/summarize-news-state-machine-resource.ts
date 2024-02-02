import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambdaPython from '@aws-cdk/aws-lambda-python-alpha';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';
import { Construct } from 'constructs';

export const addSummarizeNewsStateMachineResource = (scope: Construct): stepfunctions.StateMachine => {

    const role = new iam.Role(scope, 'SummarizeNewsStateMachineRole', {
        roleName: 'PNST-SummarizeNewsStateMachineRole',
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
                            `arn:aws:lambda:${cdk.Aws.REGION}:${cdk.Aws.ACCOUNT_ID}:function:PNST-SUMMARIZE-NEWS:*`,
                        ],
                    }),
                ]
            })
        }
    });

    const summarizeNewsFunction = getSummarizeNewsFunctionResource(scope);

    const summarizeNewsTask = new tasks.LambdaInvoke(scope, 'SummarizeNewsTask', {
        lambdaFunction: summarizeNewsFunction,
        inputPath: '$',
        outputPath: '$.Payload',
    });

    const succeed = new stepfunctions.Succeed(scope, 'SumarizeNewsucceed', {
        stateName: 'succeeded'
    });

    const definition = summarizeNewsTask
        .next(succeed);

    const stateMachine = new stepfunctions.StateMachine(scope, 'SummarizeNewsStateMachine', {
        stateMachineName: 'PNST-SUMMARIZE-NEWS',
        role,
        definitionBody: stepfunctions.DefinitionBody.fromChainable(definition),
    });

    return stateMachine;
}

const getSummarizeNewsFunctionResource = (scope: Construct): lambdaPython.PythonFunction => {
     // Lambda の実行ロールを作成
     const role = new iam.Role(scope, 'SummarizeNewsFunctionRole', {
        roleName: 'PNST-SummarizeNewsFunctionRole',
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
                            'secretsmanager:GetSecretValue',
                        ],
                        resources: [
                            '*'
                        ],
                    }),
                    new iam.PolicyStatement({
                        effect: iam.Effect.ALLOW,
                        actions: [
                            's3:GetObject',
                            's3:PutObject',
                            's3:ListObject',
                        ],
                        resources: [
                            `${cdk.Fn.importValue('PNST-bucketArn')}/*`,
                        ],
                    }),
                ]
            })
        }
    });

    return new lambdaPython.PythonFunction(scope, 'SummarizeNewsFunction', {
        functionName: 'PNST-SUMMARIZE-NEWS',
        runtime: lambda.Runtime.PYTHON_3_12,
        entry: path.resolve(__dirname, '../../../lambda/summarize_news'),
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