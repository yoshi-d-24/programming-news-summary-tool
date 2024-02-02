import json
from enums.code import Code
from summarize import run
from datetime import datetime, timedelta
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    logger.info(event)

    code_str: str = event['code']
    code: Code = Code(code_str)

    start_date: str = event['startDate']
    end_date: str = event['endDate']

    search_date_list: list[str] = get_dates_in_range(start_date=start_date, end_date=end_date)

    if (len(search_date_list) > 7):
         raise Exception("too long")

    logger.info(event)

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
    
def get_dates_in_range(start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%Y/%m/%d")
    end = datetime.strptime(end_date, "%Y/%m/%d")
    date_array = [(start + timedelta(days=x)).strftime("%Y/%m/%d") for x in range(0, (end-start).days+1)]
    return date_array