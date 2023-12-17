import scrapy
from ..items import ScraperItem


class CodezineNewsSpider(scrapy.Spider):
    name = "codezine-news"
    allowed_domains = ["codezine.jp"]
    start_urls = ["https://codezine.jp/article/t/%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9"]

    def __init__(self, feed=None, *args, **kwargs):
        super(CodezineNewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        search_date = self.date

        item_content_list = response.xpath('//div[has-class("c-articleindex_item")]')

        for item_content in item_content_list:
            title = item_content.xpath('.//p[has-class("c-articleindex_item_heading")]/a/text()').get()
            link = item_content.xpath('.//p[has-class("c-articleindex_item_heading")]/a/@href').get()
            date = item_content.xpath('.//p[has-class("c-featureindex_item_date")]/time/text()').get()
            id = int(link.replace('/article/detail/', ''))

            if search_date != date:
                continue

            tag_elements = item_content.xpath('.//div[has-class("c-articleindex_item_tags")]/ul[has-class("c-taglist")]/li/a')

            tag_list = list(map(lambda tag: tag.xpath('text()').get(), tag_elements))

            url = response.urljoin(link)
            # リンク先を訪れるためのRequestを作成し、parse_linkメソッドで処理する
            yield scrapy.Request(url=url, callback=self.parse_link, meta={'id': id, 'title': title, 'url': url, 'date': date, 'tag_list': tag_list})

    def parse_link(self, response):
        # リンク先のページの内容を取得
        paragraphs = response.xpath('//div[has-class("c-article_content")]/p/text()').getall()

        # パラグラフの文字列を結合
        content = ' '.join(paragraphs)

        id = response.meta['id']
        title = response.meta['title']
        url = response.meta['url']
        date = response.meta['date']
        tag_list = response.meta['tag_list']

        item = ScraperItem(
            id,
            title,
            url,
            date,
            content,
            tag_list)
        yield item
