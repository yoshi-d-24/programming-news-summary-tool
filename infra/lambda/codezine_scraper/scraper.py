import requests
from parser.news_parser import NewsParser
from const.domain import CODEZINE_DOMAIN
from data_access.s3.pnst_bucket_data_access import PnstBucketDataAccess

def run(search_date: str):
    url = f'https://{CODEZINE_DOMAIN}/article/t/%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9'

    response: requests.Response = requests.get(url)

    news_parser: NewsParser = NewsParser(response)
    pnst_bucket_data_access = PnstBucketDataAccess()

    news_data_list = news_parser.generate_news_data_list(search_date)
    pnst_bucket_data_access.put_news(search_date, news_data_list)

if __name__ == '__main__':
    run('2023/12/27')