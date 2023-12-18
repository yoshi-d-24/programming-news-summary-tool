import boto3
from aws_lambda_powertools import Logger
from datetime import datetime, timedelta
from model.news_data import NewsData

logger = Logger(child=True)

TABLE_NAME = 'PNST-NEWS'

dynamodb = boto3.resource('dynamodb')

class NewsTableDataAccess:
    def __init__(self):
        self.table = dynamodb.Table(TABLE_NAME)

    def batch_write(self, data_list: list[NewsData]):
        # 現在の日時を取得
        current_time = datetime.now()

        # 1ヶ月後の日時を計算
        ttl = int((current_time + timedelta(days=30)).timestamp())

        try:
            with self.table.batch_writer() as batch:
                for data in data_list:
                    batch.put_item(
                        Item={
                            'code': data.code.name,
                            'id': data.id,
                            'title': data.title,
                            'link': data.link,
                            'date': data.date,
                            'content': data.content,
                            'tag_set': data.tag_set,
                            'ttl': ttl ,
                        }
                    )
        except Exception as error:
            logger.error(error)
            raise error
