# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import xlwt
import pymysql
import re
import pymongo
# class ZhilianPipeline(object):
#     def process_item(self, item, spider):
#         return item
class ZhilianPipelineJson(object):
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

class ZhilianPipelineXls(object):
    def __init__(self):
        self.__dirName = os.path.join(os.getcwd(),'data')
        if not os.path.exists(self.__dirName):
            os.makedirs(self.__dirName)       
        self.__excelPath = os.path.join(self.__dirName,'files.xls')
        self.rows = 1                
    def open_spider(self,spider):
        self.workbook = xlwt.Workbook(encoding = "utf8")
        self.worksheet = self.workbook.add_sheet("招聘信息")
        headers = ['position', 'company_name', 'company_url', 'company_size', 'company_type', 'positionURL', 'workingExp', 'eduLevel', 'salary', 'jobName', 'city', "updateDate", "createDate", "endDate", "welfare"]
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

class ZhilianPipelineDb(object):
    def open_spider(self,spider):
        params = {
            "host":"localhost",
            "port":3306,
            "user":"root",
            "password":"123",
            "db":"zhilian",
            "charset":"utf8"
        }
        try:
            self.connection = pymysql.connect(**params)
            self.cur = self.connection.cursor()
        except Exception:
            print("数据库连接失败或者游标创建失败")
    def process_item(self,item,spider):
        sql = 'insert into zlzp_java_tj(position,company_name,company_url,company_size,company_type,positionURL,workingExp,eduLevel,salary,jobName,city,updateDate,createDate,endDate,welfare) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        param = (item['position'],item['company_name'],item['company_url'],item['company_size'],item['company_type'],item['positionURL'],item['workingExp'],item['eduLevel'],item['salary'],item['jobName'],item['city'],item['updateDate'],item['createDate'],item['endDate'],item['welfare'])
        rowscount = self.cur.execute(sql,param)
        if rowscount:
            print('写入数据成功!')
        return item
    def close_spider(self,spider):
        self.connection.commit()
        self.cur.close()
        self.connection.close()

class ZhilianPipelineMongo(object): 
    def open_spider(self,spider):
        self.myclient = pymongo.MongoClient('127.0.0.1',27017)
        self.newdb = self.myclient['zhilian']
        self.newColl = self.newdb['Tj']
    def process_item(self,item,spider):
        self.newColl.insert_one(item)

class ZhilianPipelineSalary_web(object):
    def __init__(self):
        self.__dirName = os.path.join(os.getcwd(),'data')
        if not os.path.exists(self.__dirName):
            os.makedirs(self.__dirName)       
        self.__excelPath = os.path.join(self.__dirName,'salary_web.xls')
        self.rows = 1
    
    def open_spider(self,spider):
        self.workbook = xlwt.Workbook(encoding = "utf8")
        self.worksheet = self.workbook.add_sheet("招聘信息")
        headers = ['position', 'company_name', 'company_url', 'company_size', 'company_type', 'positionURL', 'workingExp', 'eduLevel', 'salary', 'jobName', 'city', "updateDate", "createDate", "endDate", "welfare",'avg_salary']
        for i in range(len(headers)):
            self.worksheet.write(0,i,headers[i]) 
        
    def process_item(self,item,spider):
        if '互联网开发' in item['position']:
            pattarn = re.compile('(.*?)K-(.*?)K',re.S)
            lst = re.findall(pattarn,item['salary'])
            lst_0 = list(lst[0])
            avg_salary = (int(lst_0[0])+int(lst_0[1]))*500
            
            contents = [item[key] for key in item]
            contents.append(avg_salary)
            for colsIndex in range(len(contents)):
                self.worksheet.write(self.rows,colsIndex,contents[colsIndex])
            self.rows += 1
            return item
        else:
            pattarn = re.compile('(.*?)K-(.*?)K',re.S)
            lst = re.findall(pattarn,item['salary'])
            lst_0 = list(lst[0])
            avg_salary = (int(lst_0[0])+int(lst_0[1]))*500
            
            contents = [item[key] for key in item]
            contents.append(avg_salary)
            for colsIndex in range(len(contents)):
                self.worksheet.write(self.rows,colsIndex,contents[colsIndex])
            self.rows += 1
            return item

    def close_spider(self,spider):
        self.rows = 0
        self.workbook.save(self.__excelPath)

# class ZhilianPipelineSalary_ordinary(object):
#     def __init__(self):
#         self.__dirName = os.path.join(os.getcwd(),'data')
#         if not os.path.exists(self.__dirName):
#             os.makedirs(self.__dirName)       
#         self.__excelPath = os.path.join(self.__dirName,'salary_ordinary.xls')
#         self.rows = 1
    
#     def open_spider(self,spider):
#         self.workbook = xlwt.Workbook(encoding = "utf8")
#         self.worksheet = self.workbook.add_sheet("招聘信息")
#         headers = ['position', 'company_name', 'company_url', 'company_size', 'company_type', 'positionURL', 'workingExp', 'eduLevel', 'salary', 'jobName', 'city', "updateDate", "createDate", "endDate", "welfare",'avg_salary']
#         for i in range(len(headers)):
#             self.worksheet.write(0,i,headers[i]) 
        
#     def process_item(self,item,spider):
#         if '互联网开发'  not in item['position']:
#             pattarn = re.compile('(.*?)K-(.*?)K',re.S)
#             lst = re.findall(pattarn,item['salary'])
#             lst_0 = list(lst[0])
#             avg_salary = (int(lst_0[0])+int(lst_0[1]))*500
            
#             contents = [item[key] for key in item]
#             contents.append(avg_salary)
#             for colsIndex in range(len(contents)):
#                 self.worksheet.write(self.rows,colsIndex,contents[colsIndex])
#             self.rows += 1
#             return item

#     def close_spider(self,spider):
#         self.rows = 0
#         self.workbook.save(self.__excelPath)
            