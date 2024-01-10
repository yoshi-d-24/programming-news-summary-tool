import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambdaPython from '@aws-cdk/aws-lambda-python-alpha';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import { Construct } from 'constructs';

export const addCodezineScraperStateMachineResource = (scope: Construct, scraperFunction: lambdaPython.PythonFunction): stepfunctions.StateMachine => {

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


    const scraperTask = new tasks.LambdaInvoke(scope, 'ScraperTask', {
        lambdaFunction: scraperFunction,
        outputPath: '$.Payload',
    });

    const succeed = new stepfunctions.Succeed(scope, 'ScraperSucceed');

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