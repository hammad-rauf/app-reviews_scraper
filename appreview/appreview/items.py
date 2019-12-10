# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AppreviewItem(scrapy.Item):

    app_link = scrapy.Field()    
    date = scrapy.Field()
    store = scrapy.Field()
    rating = scrapy.Field()
    review = scrapy.Field()

    pass
