# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KickstarterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    project_name = scrapy.Field()
    category_name = scrapy.Field()
    project_tag = scrapy.Field() 
    funding_period = scrapy.Field()
    no_days = scrapy.Field()
    no_backers = scrapy.Field()
    money_pledged = scrapy.Field()
    starter_location = scrapy.Field()
