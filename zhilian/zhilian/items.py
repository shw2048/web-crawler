# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    position = scrapy.Field()
    
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    company_size = scrapy.Field()
    
    company_type = scrapy.Field()
    positionURL = scrapy.Field()
    workingExp = scrapy.Field()
    eduLevel = scrapy.Field()    
    
    salary = scrapy.Field()
    jobName = scrapy.Field()
    city = scrapy.Field()
    updateDate = scrapy.Field()
    createDate = scrapy.Field()
    
    endDate = scrapy.Field()
    welfare = scrapy.Field()
    

    pass
