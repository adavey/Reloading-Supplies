from cgitb import html
from numpy import product
from requests import get
from bs4 import BeautifulSoup
import psycopg2
from configparser import ConfigParser

class WebSite():
    name = 'WebSite'
    print_in_stock_only = True

    def __init__(self):
        params = self.config()
        self.conn = psycopg2.connect(**params)
        
    def config (self, filename='./database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)
        db={}
        if parser.has_section:
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section,filename))
        return db

    def process_site(self):
        self.print_checking_message()
        self.get_products()
        for record in self.products:
            self.extract_record(record)
            self.lookup_product()
            self.print_product_availability()
            self.save_results()

    def extract_record(self, record):
        self.web_product_id = record[0]
        self.manufacturer = record[1]
        self.product = record[2]
        self.size = record[3]
        self.url = record[4]

    def lookup_product():
        pass

    def print_checking_message(self):
        print('Checking ' + self.name + ' ...')

    def print_product_availability(self):
        if self.is_available:
            available_text = 'In Stock'
        else:
            available_text = 'Out of Stock'

        if available_text == 'In Stock' and self.print_in_stock_only == True:
            print('{0}: {1} {2} ({3}):  {4}'.format(self.name, self.manufacturer, self.product, self.size, available_text))
        elif self.print_in_stock_only == False:
            print('{0}: {1} {2} ({3}):  {4}'.format(self.name, self.manufacturer, self.product, self.size, available_text))

    def get_products(self):
        cur = self.conn.cursor()
        cur.execute('select wp.id, m.name, p.name, p.size, wp.url ' \
                    'from website_product wp ' \
                    'join website w on w.id = wp.website_id ' \
                    'join product p on p.id = wp.product_id ' \
                    'join manufacturer m on m.id = p.manufacturer_id ' \
                    'where w.name = %s' \
                    'order by 2, 3, 4',(self.name,))
        self.products = cur.fetchall()
        cur.close()

    def save_results(self):
        cur = self.conn.cursor()
        cur.execute('insert into check_web_product_log (web_product_id, is_available) values(%s, %s)'
                    , (self.web_product_id, self.is_available))
        self.conn.commit()
        cur.close()

class BallisticProducts(WebSite):
    name = 'Ballistic Products'

    def __init__(self):
        super().__init__()
        # self.print_in_stock_only = False

    def lookup_product(self):
        self.is_available = False
        response = get(self.url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        product_info = html_soup.find_all('td',class_ = 'plaintextbold')
        if len(product_info) > 0:
            if product_info[1].text.lower().find('in stock') != -1:
                self.is_available = True



import selenium
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging
import sys

class PrecisionReloading(WebSite):
    name = 'Precision Reloading'

    def __init__(self):
        super().__init__()

        self.opts = webdriver.ChromeOptions()
        self.opts.headless =True        
        
        # Workaround to suppress initial WebDriver Manager messages to console as specifiying log level
        # as an argument or via constructor parameter to ChromeDriverManager did not work.
        #opts.add_argument('--log_level=0')
        #opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        os.environ["WDM_LOG_LEVEL"] = str(logging.WARNING)

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.opts)

    def lookup_product(self):
        self.is_available = False
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='prodStatus']")))
            text = self.driver.find_element_by_class_name('prodStatus').text 
            if text.lower().find('in stock') != -1:
                self.is_available = True
        except Exception as e:
            print(e)
            self.is_available = False
        


class ShydasOutdoorCenter(WebSite):
    name = 'Shyda\'s Outdoor Center'

    def __init__(self):
        super().__init__()

        self.opts = webdriver.ChromeOptions()
        self.opts.headless =True        
        
        # Workaround to suppress initial WebDriver Manager messages to console as specifiying log level
        # as an argument or via constructor parameter to ChromeDriverManager did not work.
        #opts.add_argument('--log_level=0')
        #opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        os.environ["WDM_LOG_LEVEL"] = str(logging.WARNING)

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.opts)

    def lookup_product(self):
        self.is_available = False
        # print(self.url)
        self.driver.get(self.url)
        html_soup = BeautifulSoup(self.driver.page_source,  'html.parser')
        product_info = html_soup.find('p',class_ = 'availability in-stock')
        if product_info is not None:
            # print(product_info.text)
            if product_info.text.lower().find('in stock') != -1:
                self.is_available = True
            else:
                self.is_available = False
        else:
            self.is_available = False
                         
        

class Recobs(WebSite):
    name = 'Recob\'s Target Shop'

    def lookup_product(self):
        self.is_available = False
        response = get(self.url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        product_info = html_soup.find('p',class_ = 'stock in-stock')
        if product_info is not None:
            self.is_available = True

class Grafs(WebSite):
    name = 'Graf and Sons'

    def __init__(self):
        super().__init__()

        # Add header with user-agent in order to receive content.
        self.headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'}

    def lookup_product(self):
        self.is_available = False
        response = get(self.url, headers=self.headers)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        product_info = html_soup.find('td',class_ = 'swat-details-view-field odd swat-text-cell-renderer grafs-quantity-cell-renderer')
        if product_info.text.find('In Stock') != -1:
            self.is_available = True
            