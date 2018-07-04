from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from settings import *
from pymongo import MongoClient
import re


class Spider(object):
    def __init__(self, host=HOST, keyword=KEYWORD):
        self.host = host
        self.keyword = keyword
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.set_window_size(1400, 900)
        self.wait = WebDriverWait(self.driver, timeout=15)
        # MongoDB，默认链接本地
        self.client = MongoClient(host=MONGODB_URL, port=MONGODB_PORT)
        self.db = self.client[MONGODB_DB]

    def __del__(self):
        self.driver.close()
        self.client.close()

    def start(self):
        print('正在驱动浏览器...')
        total = self.get_first_page()
        for page in range(2, total+1):
            self.get_next_page(page)

    def get_first_page(self):
        self.driver.get(self.host)
        input_element = self.wait.until(EC.presence_of_element_located((By.ID, 'key')))
        input_element.clear()
        input_element.send_keys(self.keyword)
        input_element.send_keys(Keys.RETURN)
        self.wait.until(EC.presence_of_element_located((By.ID, 'J_goodsList')))
        self.get_product()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'fp-text')))
        total_page = pq(self.driver.page_source)('.fp-text').text().split('/')[-1].replace('\n', '')
        return int(total_page)

    def get_next_page(self, page_no):
        print('正在翻页：', page_no)
        # next_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'fp-next')))
        # next_element.click()
        # wait.until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, '#J_topPage > span > b'), str(page_no)))

        input_next_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input-txt')))
        input_next_element.clear()
        input_next_element.send_keys(page_no)
        submit_element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a')))
        submit_element.click()
        self.get_product()

    def get_product(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find_all('div', attrs={'class': 'gl-i-wrap'})
        for item in items:
            # 通过调转的链接获取pid
            search_str = item.find('div', attrs={'class': 'p-img'}).find('a').attrs['onclick']
            pid = re.compile('searchlog\(.*?,(.*?),.*?\)', re.S).search(search_str).group(1)
            img_element = item.find('div', attrs={'class': 'p-img'}).find('a').find('img')
            img = img_element.attrs.get('src', None)
            if img is None:
                img = img_element.attrs['data-lazy-img']
            price = item.find('div', attrs={'class': 'p-price'}).find('strong').get_text()
            title = item.find('div', attrs={'class': 'p-name'}).find('a').find('em').get_text()
            commit = item.find('div', attrs={'class': 'p-commit'}).find('strong').get_text().replace('\n', '')[:-3]
            shop = item.find('div', attrs={'class': 'p-shop'}).find('a').get_text()
            product = {
                'pid': pid,
                'img': 'http:' + img,
                'price': price,
                'title': title,
                'commit': commit,
                'shop': shop
            }
            self.print_product(product)
            print('='*50)
            self.save_to_mongo(product)

    def save_to_mongo(self, product):
        # 使用KEYWORD作为表明
        search_product = self.db[KEYWORD].find_one({'pid': product['pid']})
        if search_product is None:
            print('未找到该数据，插入该条数拒')
            self.db[KEYWORD].insert(product)
        else:
            print('已有该条数据，更新该数据')
            self.db[KEYWORD].update_one({'pid': product['pid']}, {'$set': {
                'pid': product['pid'],
                'img': product['img'],
                'price': product['price'],
                'title': product['title'],
                'commit': product['commit'],
                'shop': product['shop']
            }})

    def print_product(self, product):
        print('id：', product.get('pid', None))
        print('名称：', product.get('title', None))
        print('图片：', 'http:' + product['img'])
        print('价格：', product.get('price', None))
        print('评论数：', product.get('commit', None))
        print('店铺：', product.get('shop', None))


if __name__ == '__main__':
    spider = Spider()
    spider.start()
