import json
from summarize import run
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    summary = run(event['content'])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json;charset=UTF-8"
        },
        "body": json.dumps({
            "summary ": summary
        }, ensure_ascii=False)
    }