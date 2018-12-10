from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pyquery import PyQuery as pq
from config import *
import pymongo
import pymysql
import re
import time

from selenium.webdriver.chrome.options import Options

#搜索内容 mysql创建对应表及修改表名 mongo配置文件config.py中修改table
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"')
# chrome_options.add_argument('--proxy-server=http://27.17.45.90:43411')
prefs = {"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)
# browser = webdriver.Chrome(r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe')
wait = WebDriverWait(browser, 10)
browser.maximize_window()
def search():
    try:
        browser.get('http://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        time.sleep(2)
        input.send_keys(KEYWORD)
        time.sleep(2)
        submit.click()
        time.sleep(2)
        validate()
        print('返回')
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        print('无法获取网页')
        return total.text
    except TimeoutException:
        print('跳转报错')
        return search()

def validate():
    try:
        print('跳转成功')
        time.sleep(2)
        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static'))
        )
        button.click()
        time.sleep(2)
        name = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_username_1'))
        )
        name.clear()
        name.send_keys(USERNAME)
        time.sleep(2)
        password = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_password_1'))
        )
        password.send_keys(PWD)
        print('获取输入框2')
        time.sleep(2)
        #获取滑块
        rolling = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#nc_1_n1z'))
        )
        action =ActionChains(browser)
        action.click_and_hold(rolling)
        action.reset_actions()
        # time.sleep(5)
        action.move_by_offset(400,0)
        # action.drag_and_drop_by_offset(rolling,400,0)
        print('滑块')
        time.sleep(2)
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_SubmitStatic'))
        )
        print('获取提交按钮成功')
        # button.click()
        # name.clear()
        # name.send_keys(USERNAME)
        # password.send_keys(PWD)
        submit.click()
        print('点击提交')
    except TimeoutException:
        print('操作失败')
        return search()


def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text().replace('\n',''),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text().replace('\n',''),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)
        # save_to_mysql(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存入MongoDB成功', result) 
    except Exception:
        print('存入MongoDB失败', result)

# def save_to_mysql(item):
#     params = {
#         "host": "localhost",
#         "port": 3306,
#         "user": "root",
#         "password": "123",
#         "db": "taobao",
#         "charset": "utf8"
#     }
#     try:
#         connection = pymysql.connect(**params)
#         cur = connection.cursor()
#     except Exception:
#         print("数据库连接失败或者游标创建失败")
#     sql = 'insert into pc(title,price,deal,shop,location,image) values(%s,%s,%s,%s,%s,%s)'
#     param = (item['title'], item['price'], item['deal'], item['shop'], item['location'],item['image'])
#     rowscount = cur.execute(sql, param)
#     if rowscount:
#         print('写入数据成功!')
#     connection.commit()
#     cur.close()
#     connection.close()

def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2,total+1):
            next_page(i)
    finally:
        browser.close()

if __name__ == "__main__":
    main()