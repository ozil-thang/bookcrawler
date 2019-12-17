from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from bookstore.items import BookstoreItem

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['vinabook.com']
    start_urls = ['https://vinabook.com/']


    def parse(self, response):
        categories_sel = response.xpath('//*[contains(@data-submenu-id, "submenu")]')[1:-1]

        for category_sel in categories_sel:
            category = category_sel.xpath('.//h2/text()').extract_first()

            li_sel = category_sel.xpath('.//li[1]')

            sub_categories = li_sel.xpath('.//a/@title')[1:].extract()

            sub_categories_url = li_sel.xpath('.//a/@href')[1:].extract()

            for sub_category_url in sub_categories_url:
                yield Request(sub_category_url, callback=self.parse_sub_category)

    def parse_sub_category(self, response):
        table = response.xpath('//table')[-1]
        books_url = table.xpath('.//*[@class="product-title"]/@href').extract()
        books_url = [url.strip().strip('\n') for url in books_url]

        for url in books_url:
            yield Request(url, callback=self.parse_book)

        next_page_url = response.xpath('//*[@class="next cm-history "]/@href').extract_first()
        if next_page_url and 'page-5' not in next_page_url:
            yield Request(next_page_url, callback=self.parse_sub_category)


    def parse_book(self, response):
        title = response.xpath('//h1/text()').extract_first()

        author = response.xpath('//*[@class="author"]/text()')[-1].extract()

        datePublished = response.xpath('//*[@itemprop="datePublished"]/@content').extract_first().strip()

        numberOfPages = response.xpath('//*[@itemprop="numberOfPages"]/text()').extract_first()

        price = response.xpath('//*[contains(@id, "sec_list_price")]/text()').extract_first()

        div = response.xpath('//*[@class="full-description"]')
        description = div.xpath("string()").extract_first()
        description = description.replace('Thông tin tác giả    Nhiều Tác Giả     Vào trang riêng của tác giả   Xem tất cả các sách của tác giả', '').strip()

        image_url = response.xpath('//*[contains(@id,"det_img")]/@src').extract_first()

        category, sub_category = response.xpath('//*[@itemprop="title"]/text()')[1:3].extract()


        l = ItemLoader(BookstoreItem())
        l.add_value('title', title)
        l.add_value('author', author)
        l.add_value('datePublished', datePublished)
        l.add_value('numberOfPages', numberOfPages)
        l.add_value('price', price)
        l.add_value('description', description)
        l.add_value('image_urls', image_url)
        l.add_value('category', category)
        l.add_value('sub_category', sub_category)


        yield l.load_item()
