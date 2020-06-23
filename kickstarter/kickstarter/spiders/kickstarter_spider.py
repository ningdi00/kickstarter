from kickstarter.items import KickstarterItem
from scrapy import Spider, Request
from scrapy_splash import SplashRequest
import re

class KickstarterSpider(Spider):
    name = 'kickstarter_spider'
    allowed_urls = ['www.kickstarter.com']
    start_urls = ['https://www.kickstarter.com/discover/advanced?state=successful&sort=popularity&seed=2654646&page=1']

    def parse(self, response):
        pages = list(range(201))
        category = response.xpath('//ul[@class="js-categories columns2-sm relative z1 inline-block block-sm w50-sm"]//li/@data-category').extract()
        category_id = list(map(int,map(lambda x: re.findall('\d+',x)[0], category)))
        category_urls = [f'https://www.kickstarter.com/discover/advanced?state=successful&category_id={i}&sort=popularity&seed=2654646&page={n}' for i in category_id for n in pages[1:]]

        lua = '''
            function main(splash, args)
                assert(splash:go(args.url))
                assert(splash:wait(1))
                return splash:html()
            end
        '''
        for urls in category_urls[:1]:
            yield SplashRequest(url = urls, callback = self.parse_category_page, endpoint = 'execute', args = {'lua_source':lua})

    def parse_category_page(self, response):

        info = response.css("clamp-5 navy-500 mb3 hover-target").xpath('//a/@href').extract()

        # print('='*40)
        # print(info)
        # print('='*40)
 


money_pledged = int(''.join(re.findall('\d+',response.xpath('//div[@class="NS_campaigns__spotlight_stats"]/span/text()').extract_first())))
currency = ''.join(re.findall('[^(\d|\s|,)]',response.xpath('//div[@class="NS_campaigns__spotlight_stats"]/span/text()').extract_first()))
no_backers = int(re.findall('\d+', response.xpath('//div[@class="NS_campaigns__spotlight_stats"]/b/text()').extract_first()))
project_name = response.xpath('//span[@class="relative"]/a/text()').extract_first()
category_name = (response.xpath('//div[@class="NS_projects__category_location ratio-16-9 flex items-center"]//text()').extract()[2]).strip('\n')
starter_location = (response.xpath('//div[@class="NS_projects__category_location ratio-16-9 flex items-center"]//text()').extract()[1]).strip('\n')
goal = int("".join(re.findall('\d+',response.xpath('//div[@class="type-12 medium navy-500"]/span[@class="money"]/text()').extract_first())))
funding_period_start = response.xpath('//div[@class="NS_campaigns__funding_period"]/p/time/text()').extract()[0]
funding_period_end = response.xpath('//div[@class="NS_campaigns__funding_period"]/p/time/text()').extract()[1]
no_days = int(re.findall('\d+',"".join(response.xpath('//div[@class="NS_campaigns__funding_period"]/p/text()').extract()))[0])