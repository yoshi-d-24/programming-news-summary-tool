import json
from scraper import run
from datetime import datetime, timedelta

from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    current_date = datetime.now()
    one_day_ago = current_date - timedelta(days=1)
    search_date = one_day_ago.strftime("%Y/%m/%d")
    run(search_date)
    # run(event['search_date'])

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