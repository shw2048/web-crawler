# -*- coding:utf-8 -*-
'''
    详情页界面爬取
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from lxml import etree
import time,os,json,re
import random


chrome_options = Options()
chrome_options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"')
# chrome_options.add_argument('--proxy-server=http://112.25.6.24:80')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
prefs = {"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(driver, 5)
driver.maximize_window()

def change_detail_content():
    #创建url生成器
    # url = ('http://www.jiuxian.com/goods-' + str(i) + '.html' for i in range(100000))
    #1207 ->38805
    for i in range(37500, 100000):
        url = 'http://www.jiuxian.com/goods-' + str(i) + '.html'
        get_detail_content(url)


def get_detail_content(url):
    try:
        #调用生成器
        print(url)
        driver.get(url)
        # wait.until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'body > div.w1200'))
        # )
        html = driver.page_source
        # 获取图片地址 存入列表pic_lst
        try:
            pic_pattern = re.compile("[\s]*lbarr\[0\]=\['(.*?)function[\s]*showLN", re.S)
            result_pic = re.search(pic_pattern, html)
            pic_data = result_pic.group(1)
            txt = pic_data.replace('\n', '').replace("lbarr[1]=['", '').replace("lbarr[2]=['", '').\
                replace("lbarr[3]=['",'').replace("lbarr[4]=['", '').replace("lbarr[5]=['", ''). \
                replace("lbarr[6]=['", '').replace("lbarr[7]=['", '').replace("lbarr[8]=['", '').\
                replace("lbarr[9]=['", '').replace("lbarr[10]=['", '').replace("lbarr[11]=['", '').replace("'];", ',').replace(' ', '').replace(';', '')
            pic_lst = txt.split(',')[:-1]
            # print(pic_lst)

            doc = etree.HTML(html)

            name = str(doc.xpath('/html/body/div[5]/div[3]/div[2]/div[1]/h1/text()')[0]).strip().replace('（清仓）','')
            price = str(doc.xpath('//*[@id="nowPrice"]/span[1]/strong/text()')).replace('[','').replace(']','').replace("'",'')
            result = {
                'id':len(lst),
                'title': name,
                'price': price,
                'pic': pic_lst,
            }

            all_li = doc.xpath('/html/body/div[5]/div[5]/div[2]/div[2]/div[1]/div[1]/div[1]/ul/li')
            for li in all_li:
                li_name = str(li.xpath('span/text()')[0]).replace('：','')
                li_content = li.xpath('span/em/text()')[0]
                result[li_name] = li_content
            print(result)
            lst.append(result)
        except Exception as e:
            print(e)
        # time.sleep(random.randint(2,5))
    except TimeoutException:
        print('链接超时')

def save_to_json(data):
    filepath = os.path.join(os.getcwd(),'data')
    if not os.path.exists(filepath):
        os.mkdir(filepath)

    name = 'jiuxian_data_'+time.strftime('%m%d',time.localtime(time.time()))+'_01.json'
    filename = os.path.join(filepath,name)
    with open(filename,'w+') as fp:
        json.dump(data,fp,ensure_ascii=False)

if __name__ == '__main__':
    lst = []
    try:
        change_detail_content()
    finally:
        save_to_json(lst)
        driver.close()
