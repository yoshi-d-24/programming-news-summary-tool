import boto3
from model.news_data import NewsData
from model.summary_data import SummaryData
import json

BUCKET_NAME = 'pnst-bucket'

s3 = boto3.client('s3')

class PnstBucketDataAccess:
    def __init__(self):
        pass

    def get_news(self, search_date: str):

        key = 'news/' + search_date + '/codezine.json'

        res = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=key,
        )

        body = res['Body'].read()
        decoded = json.loads(body.decode('utf-8'))

        news = decoded['news']

        ret: list[NewsData] = []
        for n in news:
            ret.append(NewsData(
                code=n['code'],
                id=n['id'],
                title=n['title'],
                link=n['link'],
                date=n['date'],
                content=n['content'],
                tag_set=n['tagSet']
            ))
            
        return ret

    def put_summary(self, search_date: str, data_list: list[SummaryData]):

            joined = ','.join(list(map(lambda data: data.to_json(indent=0, ensure_ascii=False), data_list)))
            key = 'summary/' + search_date + '/codezine.json'
            json_string = '{"summary":[' + joined + ']}'

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=key,
                Body=json_string,
                ContentType='application/json;charset=utf8'
            )

            pass
