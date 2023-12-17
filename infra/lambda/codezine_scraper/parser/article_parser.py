from requests import Response
from bs4 import BeautifulSoup

class ArticleParser:
    def __init__(self, response: Response):
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def generate_content(self) -> str:
        content_list = self.soup.find('div', class_='c-article_body').find_all('div', class_='c-article_content')

        paragraph_list = []

        for content in content_list:
            content_paragraph_list = content.find_all('p')
            paragraph_list.append('\n\n'.join(content_paragraph.get_text(strip=True) for content_paragraph in content_paragraph_list))

        return  '\n\n'.join(paragraph for paragraph in paragraph_list).lstrip('Tweet  ')
