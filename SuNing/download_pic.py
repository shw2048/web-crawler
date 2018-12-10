#-*- coding:utf-8 -*-
import json,os,time,re
import requests

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
proxies = {'http':'http://182.92.113.148:8118'}
images = 'SN_images_'+time.strftime('%m%d',time.localtime(time.time()))
filepath = os.path.join(os.getcwd(),images)
if not os.path.exists(filepath):
    os.mkdir(filepath)

name = 'data_'+time.strftime('%m%d',time.localtime(time.time()))+'.json'
# name = 'data_1205.json'
with open('data'+os.sep+name,'r') as jsonfile:
    data = json.load(jsonfile)
    print(len(data))
    for i in range(len(data)):
        for j in range(len(data[i]['pic'])):

            pic_address = data[i]['pic'][j]
            re.compile('.*?(\d).jpg')

            pic = requests.get(pic_address, headers=headers).content
            filename = os.path.join(filepath+os.sep+str(i)+'_'+str(j)+'.jpg')
            with open(filename,'wb') as pfp:
                pfp.write(pic)
                print('{}写入完毕'.format(filename))

