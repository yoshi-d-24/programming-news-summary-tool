import json
from enum.code import Code
from summarize import run
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    code_str: str = event['code']
    code: Code = Code(code_str)
    search_date_list: list[str] = event['search_date_list']

    run(code=code, search_date_list=search_date_list)

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