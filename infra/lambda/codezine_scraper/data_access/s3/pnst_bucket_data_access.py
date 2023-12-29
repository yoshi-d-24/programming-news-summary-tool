import boto3
import json
from aws_lambda_powertools import Logger
from model.news_data import NewsData

logger = Logger(child=True)

BUCKET_NAME = 'pnst-bucket'

s3 = boto3.client('s3')

class PnstBucketDataAccess:
    def __init__(self):
        pass

    def put_news(self, search_date: str, data_list: list[NewsData]):

        joined = ','.join(list(map(lambda data: data.to_json(indent=0, ensure_ascii=False), data_list)))
        key = 'news/' + search_date + '/codezine.json'
        json_string = '{"news":[' + joined + ']}'

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json_string,
            ContentType='application/json;charset=utf8'
        )

        pass
