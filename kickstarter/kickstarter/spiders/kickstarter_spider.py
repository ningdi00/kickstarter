from kickstarter.items import KickstarterItem
from scrapy import Spider, Request
import re
import math

class KickstarterSpider(Spider):
    name = 'kickstarter_spider'
    allowed_urls = ['www.kickstarter.com']
    start_urls = ['https://www.kickstarter.com/discover/advanced?state=successful&sort=popularity&seed=2654646&page=1']

    def parse(self, response):
        pages = list(range(201))
        category = response.xpath('//ul[@class="js-categories columns2-sm relative z1 inline-block block-sm w50-sm"]//li/@data-category').extract()
        category_id = list(map(int,map(lambda x: re.findall('\d+',x)[0], category)))
        category_urls = [f'https://www.kickstarter.com/discover/advanced?state=successful&category_id={i}&sort=popularity&seed=2654646&page={n}' for i in category_id for n in pages[1:]]

        print(category_urls)

        for urls in category_urls[:50]:
            yield Request(url = urls, callback = self.parse_category_page)

    def parse_category_page(self, response):
        
