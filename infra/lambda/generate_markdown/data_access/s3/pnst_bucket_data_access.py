import boto3
from enums.code import Code
from model.summary_data import SummaryData
import json

BUCKET_NAME = 'pnst-bucket'

s3 = boto3.client('s3')

class PnstBucketDataAccess:
    def __init__(self):
        pass

    def get_summary(self, code: Code, search_date: str) -> list[SummaryData]:

        key = 'summary/' + search_date + f'/{code.value}.json'

        try:
            res = s3.get_object(
                Bucket=BUCKET_NAME,
                Key=key,
            )

            body = res['Body'].read()
            decoded = json.loads(body.decode('utf-8'))

            summary = decoded['summary']

            ret: list[SummaryData] = []
            for s in summary:
                ret.append(SummaryData(
                    code=s['code'],
                    id=s['id'],
                    title=s['title'],
                    uri=s['uri'],
                    date=s['date'],
                    summary=s['summary'],
                    tag_set=s['tagSet']
                ))
                
            return ret
        except:
            return []

    def put_markdown(self, code: Code, today: str, start_date: str, end_date:str, markdown: str):
        range_part = f'{start_date.replace('/', '')}_{end_date.replace('/', '')}'
        key = f'markdown/{today}/{range_part}/{code.value}_{range_part}.md'
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=markdown,
            ContentType='text/markdown;charset=utf8'
        )
