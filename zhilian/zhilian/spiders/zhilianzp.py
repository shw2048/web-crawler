# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ZhilianItem
from config import *

class ZlzpSpider(scrapy.Spider):
    name = 'zhilianzp'
    allowed_domains = ['www.zhaopin.com']
    start_urls = ['https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId='+city+'&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw='+setting_position+'&kt=3&lastUrlQuery=%7B%22pageSize%22:%2260%22,%22jl%22:%22531%22,%22kw%22:%22python%22,%22kt%22:%223%22%7D']
    
    
    def start_requests(self):
        for i in range(2,60):
            url ='https://fe-api.zhaopin.com/c/i/sou?start='+str(i*60-60)+'&pageSize=60&cityId='+city+'&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw='+setting_position+'&kt=3&lastUrlQuery=%7B%22p%22:'+str(i)+',%22pageSize%22:%2260%22,%22jl%22:%22531%22,%22kw%22:%22python%22,%22kt%22:%223%22%7D'
            yield scrapy.Request(url,callback=self.parse)

        # url = 'https://fe-api.zhaopin.com/c/i/sou?start=60&pageSize=60&cityId=531&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3&lastUrlQuery=%7B%22p%22:2,%22pageSize%22:%2260%22,%22jl%22:%22531%22,%22kw%22:%22python%22,%22kt%22:%223%22%7D'
        # yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        print(type(response.text))
        result = json.loads(response.text)
        # print(type(result))
        item = ZhilianItem() 
        lst = result['data']['results']
        for i in lst:
            # print(i)
            # print(i['jobType']['display'])
            # print(i['company']['name'])
            
            item['position'] = i['jobType']['display']
            item['company_name'] = i['company']['name']
            item['company_url'] = i['company']['url']
            item['company_size'] = i['company']['size']['name'] 
            item['company_type'] = i['company']['type']['name']
            item['positionURL'] = i['positionURL']
            item['workingExp'] = i['workingExp']['name']
            item['eduLevel'] = i['eduLevel']['name']
            item['salary'] = i['salary']
            item['jobName'] = i['jobName'].replace('\xa0','')
            item['city'] = i['city']['display']
            item['updateDate'] = i['updateDate']
            item['createDate'] = i['createDate']
            item['endDate'] = i['endDate']
            item['welfare'] = (','.join(i['welfare']))
        # for kv in result['data']['results']:
        #     for field in item.fields:
        #         if field in kv.keys():
        #             item[field] = kv.get(field)                       
            yield item
        pass
        
