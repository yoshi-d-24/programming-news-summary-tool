# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from .items import ScraperItem
from .data_access.dynamodb.news_table_data_access import NewsData, put


class ScraperPipeline:
    def process_item(self, item: ScraperItem, spider):
        int_date = int(datetime.strptime(item.date, "%Y/%m/%d").timestamp())
    
        data = NewsData(
            id=item.id,
            title=item.title,
            link=item.link,
            date=int_date,
            content=item.content,
            tag_list=item.tag_list
        )

        put(code='codezine', data=data)
        return item
