import boto3
from datetime import datetime, timedelta
from dataclasses import dataclass

TABLE_NAME = 'PNST-NEWS'

dynamodb = boto3.client('dynamodb')

@dataclass
class NewsData():
    id: int
    title: str
    link: str
    date: int
    content: str
    tag_list: list[str]

def put(code: str, data: NewsData):
    # 現在の日時を取得
    current_time = datetime.now()

    # 1ヶ月後の日時を計算
    ttl = int((current_time + timedelta(days=30)).timestamp())

    options = {
        'TableName': TABLE_NAME,
        'Item': {
            'code': {'S': code},
            'id': {'N': str(data.id)},
            'title': {'S': data.title},
            'link': {'S': data.link},
            'date': {'N': str(data.date)},
            'content': {'S': data.content},
            'tag_list': {'SS': data.tag_list},
            'ttl': {'N': str(ttl) },
        },
    }
    dynamodb.put_item(**options)
