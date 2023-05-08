import scrapy
import logging
import time
from datetime import datetime
from pprint import pprint
from lxml import html

from scrapy.http import HtmlResponse

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from _ast import Try



class Book24Spider(scrapy.Spider):
    
    name = "book24_ru"
    allowed_domains = ['book24.ru']
    start_urls = [f"https://book24.ru/search/?q=python"]
    
    # def __init__(self, name, **kwargs):
    #     super().__init__(name,**kwargs)
    #     self.name = "book24_ru"
    #     self.allowed_domains = ['book24.ru']
    #    self.start_urls = [f"https://book24.ru/search/?q={kwargs.get('query')}"]

    def parse(self, response:HtmlResponse):
        self.log("  --> Requesting URL {}".format(response.url), logging.INFO)

        response_text = self.make_selenium_get_request_for_lazy(response.url);
        html_page = html.fromstring(response_text)

        
        
        # Parsing book info:-------------------------------------------------------------
        # driver = self.make_selenium(response.url)
        # elements = driver.find_elements(By.XPATH, "//article[contains(@class,'product-card')]/div[contains(@class,'image-holder')]/a/picture/source")
        # for element in elements:
        #     self.log("  --> imgs {}".format(element.get_property("srcset")), logging.INFO)
        # driver.close()

        product_cards = html_page.xpath("//article[contains(@class,'product-card')]/div[contains(@class,'image-holder')]/a/picture/source/@srcset")
        for product_card in product_cards:
            self.log("  --> imgs {}".format(product_card), logging.INFO)

        
        # Parsing the next books pages:--------------------------------------------------
        self.log("  --> Received response body:\n{}".format(response_text), logging.DEBUG)
        next_page_url = html_page.xpath("//a[contains(@class,'pagination__item _link _button _next smartLink')]/@href")[0]
        next_page_url = "https://book24.ru{}".format(next_page_url)
        self.log("  --> NexPageUrl {}".format(next_page_url), logging.INFO)
        # The yield is stopped by the IndexOutOfBoudsError:
        yield response.follow(next_page_url,callback=self.parse)
        #----------(parsing the next books pages)----------------------------------------


        # product_cards = html_page.xpath("//article[contains(@class,'product-card')]/div[contains(@class,'image-holder')]/a/picture/img") #"//article[@class='product-card']")
        # for product_card in product_cards:
            #clazz = product_card.xpath("@class")[0]
            #if clazz == 'product-card':
            #elements = product_card.find_class("product-card__image-holder")[0].find_class("product-card__picture")[0].find_class("product-card__image ls-is-cached lazyloaded _loaded")[0]#find_class("product-card__image ls-is-cached lazyloaded _loaded")[0]
            # self.log("  --> imgs {}".format(product_card), logging.INFO)
                
            #elements = product_card.xpath("//div[contains(@class,'__content')]/a/@title")[0];
            #self.log("  --> imgs {}".format(clazz), logging.INFO)
            
        #----------(parsing book info)---------------------------------------------------
    
    def make_selenium_get_request_for_lazy (self,url):
        driver = self.make_selenium(url)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10);
        # driver.execute_script("window.scrollTo(0, 0);")
        #elements = driver.find_elements(By.XPATH,"//article[contains(@class,'product-card')]/div")
        #for element in elements:
        #    try:
        #        element.click()
        #        driver.execute_script("window.history.go(-1)")
        #    except:
        #        self.log("Not clickable: {}",logging.INFO);
            
        # article_elements = driver.find_elements(By.TAG_NAME,"article")
        # for article_element in article_elements:
        #     article_element.click()
        #     self.log("Clicked element: {}".format(article_element),logging.INFO);
        html_string = driver.page_source
        driver.close()
        return html_string
        
        
    #
    # This method employes the selenium approach for parsing the requested URL.
    # It' s used for removing auto blocking and comfortable executing JS scripts
    #  
    # def make_selenium_get_request_3(self,url):
    #    driver = self.make_selenium(url)
    #    html_string = driver.page_source
    #    driver.close()
    #    return html_string
    
    def make_selenium(self,url):
       chrome_options = Options()
       chrome_options.add_argument("--headless")
       chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
       driver = webdriver.Chrome(chrome_options=chrome_options)
       driver.get(url)
       
       header_list = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//article[contains(@class,'product-card')]/div[contains(@class,'image-holder')]/a/picture/img")))
       self.log("  --> Header list {}".format(header_list), logging.DEBUG);
       return driver;

