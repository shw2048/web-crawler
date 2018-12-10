# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title1 = scrapy.Field()
    title2 = scrapy.Field()
    title3 = scrapy.Field()
    play = scrapy.Field()
    score = scrapy.Field()
    count = scrapy.Field()
    inq = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
    classify = scrapy.Field()
    # pic = scrapy.Field()
    image_url = scrapy.Field() 
    image = scrapy.Field()    
    last_updated = scrapy.Field(serializer = str)
    pass
