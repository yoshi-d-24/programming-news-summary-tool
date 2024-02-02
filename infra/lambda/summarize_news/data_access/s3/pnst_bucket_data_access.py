import boto3
from model.news_data import Code, NewsData
from model.summary_data import SummaryData
import json
from enums.code import Code


BUCKET_NAME = 'pnst-bucket'

s3 = boto3.client('s3')

class PnstBucketDataAccess:
    def __init__(self):
        pass

    def get_news(self, code: Code, search_date: str):

        key = 'news/' + search_date + f'/{code.value}.json'

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

    def exist_summary(self, code: Code, search_date: str) -> bool:
        key = 'summary/' + search_date + f'/{code.value}.json'
        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=key)
            return True
        except:
            return False

    def put_summary(self, code: Code, search_date: str, data_list: list[SummaryData]):

            joined = ','.join(list(map(lambda data: data.to_json(indent=0, ensure_ascii=False), data_list)))
            key = 'summary/' + search_date + f'/{code.value}.json'
            json_string = '{"summary":[' + joined + ']}'

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=key,
                Body=json_string,
                ContentType='application/json;charset=utf8'
            )

            pass
