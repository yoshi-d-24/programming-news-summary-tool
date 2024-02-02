import boto3
from enum.code import Code
from model.submmary_data import SummaryData
import json

BUCKET_NAME = 'pnst-bucket'

s3 = boto3.client('s3')

class PnstBucketDataAccess:
    def __init__(self):
        pass

    def get_summary(self, code: Code, search_date: str):

        key = 'summary/' + search_date + f'/{code.value}.json'

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
                id=s['id'],
                title=s['title'],
                uri=s['uri'],
                date=s['date'],
                summary=s['summary'],
                tag_set=s['tagSet']
            ))
            
        return ret
