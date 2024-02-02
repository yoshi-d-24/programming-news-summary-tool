import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambdaPython from '@aws-cdk/aws-lambda-python-alpha';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';
import { Construct } from 'constructs';

export const addGenerateMarkdownStateMachineResource = (scope: Construct): stepfunctions.StateMachine => {

    const role = new iam.Role(scope, 'GenerateMarkdownStateMachineRole', {
        roleName: 'PNST-GenerateMarkdownStateMachineRole',
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
                            `arn:aws:lambda:${cdk.Aws.REGION}:${cdk.Aws.ACCOUNT_ID}:function:PNST-GENERATE-MARKDOWN:*`,
                        ],
                    }),
                ]
            })
        }
    });

    const generateMarkdownFunction = getGenerateMarkdownFunctionResource(scope);

    const generateMarkdownTask = new tasks.LambdaInvoke(scope, 'GenerateMarkdownTask', {
        lambdaFunction: generateMarkdownFunction,
        inputPath: '$',
        outputPath: '$.Payload',
    });

    const succeed = new stepfunctions.Succeed(scope, 'GenerateMarkdownSucceed', {
        stateName: 'succeeded'
    });

    const definition = generateMarkdownTask
        .next(succeed);

    const stateMachine = new stepfunctions.StateMachine(scope, 'GenerateMarkdownStateMachine', {
        stateMachineName: 'PNST-GENERATE-MARKDOWN',
        role,
        definitionBody: stepfunctions.DefinitionBody.fromChainable(definition),
    });

    return stateMachine;
}

const getGenerateMarkdownFunctionResource = (scope: Construct): lambdaPython.PythonFunction => {
    // Lambda の実行ロールを作成
    const role = new iam.Role(scope, 'GenerateMarkdownFunctionRole', {
        roleName: 'PNST-GenerateMarkdownFunctionRole',
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
                            's3:GetObject',
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

    return new lambdaPython.PythonFunction(scope, 'GenerateMarkdownFunction', {
        functionName: 'PNST-GENERATE-MARKDOWN',
        runtime: lambda.Runtime.PYTHON_3_12,
        entry: path.resolve(__dirname, '../../../lambda/generate_markdown'),
        index: 'index.py',
        handler: 'handler',
        memorySize: 256,
        architecture: lambda.Architecture.ARM_64,
        timeout: cdk.Duration.minutes(5),
        logFormat: lambda.LogFormat.JSON,
        applicationLogLevel: lambda.ApplicationLogLevel.INFO,
        role,
    })
}