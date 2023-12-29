import requests
from parser.news_parser import NewsParser
from const.domain import CODEZINE_DOMAIN
from data_access.dynamodb.news_table_data_access import NewsTableDataAccess

def run(search_date: str):
    url = f'https://{CODEZINE_DOMAIN}/article/t/%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9'

    response: requests.Response = requests.get(url)

    news_parser: NewsParser = NewsParser(response)
    news_table_data_access = NewsTableDataAccess()

    news_data_list = news_parser.generate_news_data_list(search_date)
    news_table_data_access.batch_write(news_data_list)


if __name__ == '__main__':
    run('2023/12/15')