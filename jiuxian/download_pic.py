#-*- coding:utf-8 -*-
import json,os,time,re
import requests

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
proxies = {'http':'http://182.92.113.148:8118'}
# images = 'images_'+time.strftime('%m%d',time.localtime(time.time()))
# images = 'images_'+time.strftime('%m%d',time.localtime(time.time()))+'_01'
images = 'jiuxian_images_1207_01'
filepath = os.path.join(os.getcwd(),images)
if not os.path.exists(filepath):
    os.mkdir(filepath)

# name = 'jiuxian_data_'+time.strftime('%m%d',time.localtime(time.time()))+'.json'
# name = 'jiuxian_data_'+time.strftime('%m%d',time.localtime(time.time()))+'_01.json'
name = 'jiuxian_data_1207_01.json'
with open('data'+os.sep+name,'r') as jsonfile:
    data = json.load(jsonfile)
    print(len(data))
    for i in range(len(data)):
        for j in range(len(data[i]['pic'])):

            pic_address = data[i]['pic'][j]

            lst = pic_address.split('.')
            lst[-2] = lst[-2][:-1] + '6'
            pic_address = ('.').join(lst)

            pic = requests.get(pic_address, headers=headers).content
            filename = os.path.join(filepath+os.sep+str(i)+'_'+str(j)+'.jpg')
            with open(filename,'wb') as pfp:
                pfp.write(pic)
                print('{}写入完毕'.format(filename))

