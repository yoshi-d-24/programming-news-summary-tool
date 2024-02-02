import json
from generate import run
from aws_lambda_powertools import Logger
from enums.code import Code

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    logger.info(event)
    code_str: str = event['code']
    code: Code = Code(code_str)

    start_date: str = event['startDate']
    end_date: str = event['endDate']


    run(code=code, start_date=start_date, end_date=end_date)

    try:
        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "application/json;charset=UTF-8"
            },
            'body': json.dumps({
            }, ensure_ascii=False)
        }
    except Exception as error:
            logger.error(error)
            raise error
