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
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import time,os,json,re
import random


chrome_options = Options()
chrome_options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"')
# chrome_options.add_argument('--proxy-server=http://182.92.113.148:8118')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
prefs = {"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(driver, 10)
driver.maximize_window()

def search_content():
    # 滑动滚动条到底部
    js = "window.scrollTo(0, document.body.scrollHeight)"
    driver.execute_script(js)  # 执行js，将滚动条滑到最下方
    time.sleep(3)
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="bottom_pager"]'))
    )
    # total = wait.until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="bottom_pager"]/div/span[@class="page-more"]/text()'))
    # )
    # pattern = re.compile("[^0-9]")
    # total = re.search(pattern, total)[1]
    # print(total)
    html = driver.page_source
    doc = etree.HTML(html)
    lis = doc.xpath('//*[@class="general clearfix"]/li')
    total = int(doc.xpath('//span[@class="page-more"]/text()')[0][1:3])
    # print(total)
    print(len(lis))
    for li in lis:
        url = 'https:'+str(li.xpath('div[@class="item-bg"]//a/@href')[0])
        print(url)
        detail_content(url)
    return total

def detail_content(url):
    js_open = 'window.open("'+url+'")'
    driver.execute_script(js_open)
    handles = driver.window_handles
    for handle in handles:
        if handle!=driver.current_window_handle:
            driver.switch_to_window(handle)
    time.sleep(2)
    parse()
    driver.close()
    driver.switch_to_window(handles[0])

def parse():
    html = driver.page_source
    doc = etree.HTML(html)
    result = {}
    result['id'] = len(lst)
    if len(doc.xpath('//*[@id="itemDisplayName"]/text()'))==0:
        pass
    else:
        title = str(doc.xpath('//*[@id="itemDisplayName"]/text()')[0]).replace('\n','').replace('\t','')
        result['title'] = title

    if len(doc.xpath('//span[@class="mainprice"]/text()'))==0:
        pass
    else:
        price = str(doc.xpath('//span[@class="mainprice"]/text()')[0]).replace('.', '')
        result['price'] = price

    all_li = doc.xpath('//*[@id="kernelParmeter"]/ul/li')
    for li in all_li:
        item = li.xpath('text()')
        if len(item)==0:
            item = str(li.xpath('span/text()')[0]).split('：')
            item[1] = li.xpath('span/a/text()')[0]
            result[item[0]] = item[1]
        else:
            item = item[0].split('：')
            result[item[0]] = item[1]

    pic_li = doc.xpath('//*[@id="imgZoom"]/div[3]/div/ul/li')
    pic_lst = []
    for li in pic_li:
        pic = 'https:'+li.xpath('a/img/@src-medium')[0]
        pic_lst.append(pic)
    result['pic'] = pic_lst
    print(result)
    lst.append(result)


def next_page(page):

    js = 'window.scrollTo(document.body.scrollHeight, 12000)'
    driver.execute_script(js)
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#bottomPage'))
    )

    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#bottom_pager > div > a.page-more.ensure'))
    )
    input.clear()
    input.send_keys(page)
    submit.click()
    # driver.find_element_by_css_selector('#bottom_pager > div > a.page-more.ensure').click()
    time.sleep(2)
    search_content()

def save_to_json(data):
    filepath = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(filepath):
        os.mkdir(filepath)

    name = 'data_' + time.strftime('%m%d', time.localtime(time.time())) + '.json'
    filename = os.path.join(filepath, name)
    with open(filename, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False)

def main():
    try:
        driver.get('https://search.suning.com/%E9%85%92/')
        total = search_content()
        for i in range(39,50+1):
            next_page(i)
    finally:
        save_to_json(lst)

if __name__ == '__main__':

    lst = []
    main()