from datetime import datetime
import requests
from bs4 import BeautifulSoup
from model.news_data import NewsData, Code
from parser.article_parser import ArticleParser
from const.domain import CODEZINE_DOMAIN

class NewsParser:
    def __init__(self, response: requests.Response):
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def __find_article_list(self):
        return self.soup.find_all('div', class_='c-articleindex_item')

    @staticmethod
    def __find_id(link: str) -> str:
        return int(link.replace('/article/detail/', ''))

    @staticmethod
    def __find_title(article) -> str:
        return article.find('p', class_='c-articleindex_item_heading').find('a').get_text(strip=True)

    @staticmethod
    def __find_link(article) -> str:
        return article.find('p', class_='c-articleindex_item_heading').find('a')['href']

    @staticmethod
    def __find_date(article) -> str:
        return article.find('p', class_='c-featureindex_item_date').find('time').get_text(strip=True)

    @staticmethod
    def __find_tag_set(article) -> set[str]:
        tag_elements = article.find('div', class_='c-articleindex_item_tags').find('ul', class_='c-taglist').find('li').find('a')
        return set(map(lambda tag: tag.get_text(strip=True), tag_elements))

    def generate_news_data_list(self, search_date: str) -> list[NewsData]:
        article_list = self.__find_article_list()

        news_data_list = []

        for article in article_list:
            date = NewsParser.__find_date(article)

            if date != search_date:
                continue

            title = NewsParser.__find_title(article)
            link = NewsParser.__find_link(article)
            id = NewsParser.__find_id(link)
            tag_set = NewsParser.__find_tag_set(article)

            link_response = requests.get(f'https://{CODEZINE_DOMAIN}' + link)

            article_parser = ArticleParser(link_response)
            content = article_parser.generate_content()

            int_date = int(datetime.strptime(date, "%Y/%m/%d").timestamp())

            news_data_list.append(NewsData(
                code=Code.CODEZINE,
                id=id,
                title=title,
                link=link,
                date=int_date,
                content=content,
                tag_set=tag_set
            ))

        return news_data_list




