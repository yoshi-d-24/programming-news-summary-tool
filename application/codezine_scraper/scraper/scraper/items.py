# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

@dataclass
class ScraperItem():
    id: int
    title: str
    link: str
    date: str
    content: str
    tag_list: list[str]