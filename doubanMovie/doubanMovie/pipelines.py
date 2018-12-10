# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt
import os
import json
import pymysql
import requests
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
# from doubanMovie.spiders.moviespider import MoviespiderSpider
  
class DoubanmoviePipelineXls(object):
    def __init__(self):
        self.__dirName = os.path.join(os.getcwd(),'data')
        if not os.path.exists(self.__dirName):
            os.makedirs(self.__dirName)       
        self.__excelPath = os.path.join(self.__dirName,'files.xls')
        self.rows = 1                
    def open_spider(self,spider):
        self.workbook = xlwt.Workbook(encoding = "utf8")
        self.worksheet = self.workbook.add_sheet("电影排名")
        headers = ['title1', 'title2', 'title3', 'play', 'score', 'count', 'inq', 'image_url','classify', 'director', 'actor']
        for i in range(len(headers)):
            self.worksheet.write(0,i,headers[i]) 
        
    def process_item(self,item,spider):
        contents = [item[key] for key in item]
        # headers = [key for key in item]
        # print(headers)
        for colsIndex in range(len(contents)):
            self.worksheet.write(self.rows,colsIndex,contents[colsIndex])
        self.rows += 1
        return item
    def close_spider(self,spider):
        self.rows = 0
        self.workbook.save(self.__excelPath)

class DoubanmoviePipelineJson(object):
    def __init__(self):
        self.__dirName = os.path.join(os.getcwd(),'data')
        if not os.path.exists(self.__dirName):
            os.makedirs(self.__dirName)       
        self.__jsonPath = os.path.join(self.__dirName,'files.json')
    def open_spider(self,spider):
        self.jsonFile = open(self.__jsonPath,'w',encoding="utf8")
        self.jsonFile.write("[")
        self.i = 1
    def process_item(self,item,spider):
        if self.i == 1:
            content = json.dumps(dict(item),ensure_ascii=False)
            self.jsonFile.write(content)
            self.i = 0
        else:
            content = ',\n'+json.dumps(dict(item),ensure_ascii=False)
            self.jsonFile.write(content)
        return item
    def close_spider(self,spider):
        self.jsonFile.write("]")
        self.jsonFile.close()

class DoubanmoviePipelineDb(object):
    def open_spider(self,spider):
        params = {
            "host":"localhost",
            "port":3306,
            "user":"root",
            "password":"123456",
            "db":"top250",
            "charset":"utf8"
        }
        try:
            self.connection = pymysql.connect(**params)
            self.cur = self.connection.cursor()
        except Exception:
            print("数据库连接失败或者游标创建失败")
    def process_item(self,item,spider):
        sql = 'insert into top250(title1,title2,title3,play,score,count,inq,classify,director,actor) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        param = (item['title1'],item['title2'],item['title3'],item['play'],item['score'],item['count'],item['inq'],item['classify'],item['director'],item['actor'])
        rowscount = self.cur.execute(sql,param)
        if rowscount:
            print('写入数据成功!')
        return item
    def close_spider(self,spider):
        self.connection.commit()
        self.cur.close()
        self.connection.close()

# class DoubanmoviePipelinePic(object):
#     def open_spider(self,spider):
#         self.__dirName = os.path.join(os.getcwd(),'pic')
#         if not os.path.exists(self.__dirName):
#             os.makedirs(self.__dirName)

#     def process_item(self,item,spider):
#         response = requests.get(item['pic'])
#         pic_0 = response.content
#         with open(self.__dirName+os.sep+os.path.basename(item['pic']),'wb') as picFile:
#             picFile.write(pic_0)

class DoubanmoviePipelineImg(ImagesPipeline):
    def get_media_requests(self,item,info):
        yield scrapy.Request(item['image_url'])
    
    def item_completed(self,results,item,info):
        if not results[0][0]:
            raise DropItem("下载失败")
        return item
    
    def file_path(self, request, response=None, info=None):
        filename = os.path.basename(request.url)
        return filename