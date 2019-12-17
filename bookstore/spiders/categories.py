from scrapy import Spider
from scrapy.http import Request

class CategoriesSpider(Spider):
    name = 'categories'
    allowed_domains = ['vinabook.com']
    start_urls = ['https://vinabook.com/']


    def parse(self, response):
        categories_sel = response.xpath('//*[contains(@data-submenu-id, "submenu")]')[1:-1]

        for category_sel in categories_sel:
            category = category_sel.xpath('.//h2/text()').extract_first()

            li_sel = category_sel.xpath('.//li[1]')

            sub_categories = li_sel.xpath('.//a/@title')[1:].extract()

            yield {
                'category': category,
                'sub_categories': sub_categories
            }

