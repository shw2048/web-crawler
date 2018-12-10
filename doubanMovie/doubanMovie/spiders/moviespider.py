# -*- coding: utf-8 -*-
import scrapy
from ..items import DoubanmovieItem

class MoviespiderSpider(scrapy.Spider):
    name = 'moviespider'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):

        movie_items = response.xpath('//div[@class="item"]')
        print(movie_items)
        for item in movie_items:
            movie = DoubanmovieItem()
            movie['title1'] = item.xpath('div[@class="info"]/div[@class="hd"]/a/span[@class="title"][1]/text()').extract_first()
            movie['title2'] = str(item.xpath('div[@class="info"]/div[@class="hd"]/a/span[@class="title"][2]/text()').extract_first()).replace('\xa0','').replace('/','').replace(' ','')
            movie['title3'] = item.xpath('div[@class="info"]/div[@class="hd"]/a/span[@class="other"][1]/text()').extract_first().replace('\xa0','').replace(' ','')
            movie['play'] = item.xpath('div[@class="info"]/div[@class="hd"]/span/text()').extract_first()           
            movie['score'] = item.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            movie['count'] = item.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[4]/text()').extract_first()
            movie['inq'] = item.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()').extract_first()
            # movie['pic'] = item.xpath('div[@class="pic"]/a/img/@src').extract_first()
            movie['image_url'] = item.xpath('div[@class="pic"]/a/img/@src').extract_first()
            try:
                str_0 = str(item.xpath('div[@class="info"]/div[@class="bd"]/p[@class]/text()').extract()).replace('\\xa0','').replace(' ','').replace('\\n','').replace('[','').replace(']','').replace(",'',''",'').replace("'",'')
                lst = str_0.split(',')
                str_1 = lst[0][3:lst[0].index('主演')]                                                                                   
                str_2 = lst[0][lst[0].index('主演')+3:]
                movie['classify'] = lst[1]
                movie['director'] = str_1
                movie['actor'] = str_2 
            except Exception:
                movie['actor'] = None         
            yield movie
        pass
      
        next_page = response.css('span.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page,callback = self.parse)
            
