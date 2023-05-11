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

        # Downloading HTML -text:--------------------------------------------------------
        response_text = self.make_selenium_get_request_for_lazy(response.url);
        html_page = html.fromstring(response_text)
        #----------(downloading HTML -text)----------------------------------------------
        
        
        # Parsing book info:-------------------------------------------------------------
        product_cards = html_page.xpath("//article[@class='product-card']")
        for cnt,product_card in enumerate(product_cards):

            book_src = self.extract(root=product_card,xpath="div[contains(@class,'image-holder')]/a/@href")
            picture_src_data = self.extract(root=product_card,xpath="div[contains(@class,'image-holder')]/a/picture/source/@data-srcset").split(" ")[0]
            book_content = self.extract(root=product_card,xpath="div[contains(@class,'content')]")
            
            book_data = self.make_book_info( book_element=book_content, book_src=book_src, picture_src_data=picture_src_data )
            yield book_data;

        
        # Parsing the next books pages:--------------------------------------------------
        self.log("  --> Received response body:\n{}".format(response_text), logging.DEBUG)
        next_page_url = html_page.xpath("//a[contains(@class,'pagination__item _link _button _next smartLink')]/@href")[0]
        next_page_url = "https://book24.ru{}".format(next_page_url)
        self.log("  --> NexPageUrl {}".format(next_page_url), logging.INFO)
        # The yield is stopped by the IndexOutOfBoudsError:
        yield response.follow(next_page_url,callback=self.parse)
        #----------(parsing the next books pages)----------------------------------------

        
    def make_book_info (self,book_element,book_src,picture_src_data):
        
        price_div = self.extract(root=book_element,xpath="div[contains(@class,'card-price')]")
        current_price_div = self.extract(root=price_div,xpath="div[@class='product-card-price__current']")
        old_price_div = self.extract(root=price_div,xpath="div[@class='product-card-price__old']")
        
        if "https:" not in picture_src_data:
            picture_src_data = "https:{}".format(picture_src_data)
        
        book_info={
            'src':book_src,
            'title': self.extract(root=book_element,xpath="a[contains(@class,'card__name')]",is_text=True),
            'author': self.extract(root=book_element,xpath="div[contains(@class,'card__authors')]/span",is_text=True),
            'img_src':picture_src_data,
            'price':self.extract(root=current_price_div,xpath="span[@class='app-price']",is_text=True),
            'old_price':self.extract(root=old_price_div,xpath="span[@class='app-price product-card-price__old-value']",is_text=True),
            'discount':self.extract(root=old_price_div,xpath="span[@class='product-card-price__discount']",is_text=True)
            }
        
        self.log("  --> New book {}".format(book_info), logging.INFO)
        return book_info;
    
    def extract (self,root,xpath,is_text=False):
        if root is None: return None
        else:
            elements = root.xpath(xpath)
            if elements is None: return None
            else:
                if len(elements)>0:
                    if is_text == False:
                        return elements[0]
                    else:
                        return elements[0].text_content()
                else: return None        
    
    def make_selenium_get_request_for_lazy (self,url):
        driver = self.make_selenium(url)
        time.sleep(6);
        html_string = driver.page_source
        driver.close()
        return html_string
    
    def make_selenium(self,url):
       chrome_options = Options()
       chrome_options.add_argument("--headless")
       chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
       driver = webdriver.Chrome(chrome_options=chrome_options)
       driver.get(url)
       
       header_list = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//article[contains(@class,'product-card')]/div[contains(@class,'image-holder')]/a/picture/img")))
       self.log("  --> Header list {}".format(header_list), logging.DEBUG);
       return driver;

