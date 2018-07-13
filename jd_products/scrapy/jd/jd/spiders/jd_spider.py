from scrapy import Spider
from scrapy.http import Request
from ..items import JdItem
import re


class JD_spider(Spider):
    name = 'jd'
    base_url = 'https://www.jd.com'
    page_count = -1
    current_page_no = 1

    def start_requests(self):
        yield Request(self.base_url, callback=self.parse, meta={'keyword': self.settings['KEYWORD'], 'page': self.current_page_no}, dont_filter=True)

    def parse(self, response):
        for p in response.css('.gl-i-wrap'):
            search_str = p.css('.p-img a::attr("onclick")').extract_first()
            pid = re.compile('searchlog\(.*?,(.*?),.*?\)', re.S).search(search_str).group(1)
            img = p.css('.p-img a img::attr("src")').extract_first()
            if img is None:
                img = p.css('.p-img a img::attr("data-lazy-img")').extract_first()
            if img is None:
                img = p.css('.p-img a img::attr("source-data-lazy-img")').extract_first()
            price = p.css('.p-price strong i::text').extract_first()
            title = ' '.join(p.css('.p-name.p-name-type-2 a em::text').extract())
            commit = p.css('.p-commit strong a::text').extract_first()
            shop = p.css('.p-shop span a::text').extract_first()

            item = JdItem()
            item['pid'] = pid
            item['title'] = title
            item['image'] = img
            item['price'] = price
            item['commit'] = commit
            item['shop'] = shop

            item.show()
            yield item

        # 取出总页数，执行翻页
        self.page_count = int(response.css('.p-skip em b::text').extract_first()) if self.page_count == -1 else self.page_count
        if self.current_page_no < self.page_count:
            self.current_page_no += 1
            print('i = ', self.current_page_no)
            yield Request(self.base_url, callback=self.parse, meta={'keyword': '空气净化器', 'page': self.current_page_no}, dont_filter=True)
