import json
from summarize import run
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    tag_set: set[str] = event['tagSet']
    summary: str = run(event['content'])

    try:
        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "application/json;charset=UTF-8"
            },
            'body': json.dumps({
                'label': label,
                'summary': summary
            }, ensure_ascii=False)
        }
    except Exception as error:
            logger.error(error)
            raise error