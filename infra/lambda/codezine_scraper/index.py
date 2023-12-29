import json
from scraper import run
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    run(event['search_date'])

    try:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json;charset=UTF-8',
            },
            'body': json.dumps({
                'result': 'success'
            })
        }
    except Exception as error:
            logger.error(error)
            raise error