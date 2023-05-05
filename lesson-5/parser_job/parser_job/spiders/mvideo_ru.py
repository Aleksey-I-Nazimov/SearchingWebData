import scrapy
import time
from datetime import datetime
from pprint import pprint
from lxml import html

from selenium.webdriver.chrome.options import Options
from selenium import webdriver



class MvideoRuSpider(scrapy.Spider):
    
    name = 'mvideo_ru'
    
    allowed_domains = ['mvideo.ru','numamo.org']
    
    start_urls = ['https://www.mvideo.ru/televizory-i-cifrovoe-tv-1/televizory-65/f/tolko-v-nalichii=da']

    # Для пользования сайтом необходимо включить Javascript в Вашем браузере.


    def parse(self, response):
        
        print("  --> Requesting URL {}".format(response.url))
        response_text = self.make_selenium_get_request_10(response.url);
        html_page = html.fromstring(response_text)
        next_page_url = html_page.xpath("//a[contains(@class,'page-link icon ng-star-inserted')]/@href")[0]
        print("  --> NexPageUrl {}".format(next_page_url))

        yield response.follow(next_page_url,callback=self.parse)
        
        tv_list = html_page.xpath("//div[contains(@class,'product-cards-layout__item')]");
        for tv in tv_list:
            model_name = tv.xpath("//div[contains(@class,'product-title product-title--list')]/a")[0].text_content()
            model_price = tv.xpath("//span[contains(@class,'price__main-value')]")[0].text_content();
            yield {
                'model':model_name,
                'price':model_price,
                'date':str(datetime.now())
                }
    
    
    def make_selenium_get_request_10(self,url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        time.sleep(10)
        html_string = driver.page_source
        driver.close()
        return html_string;
        
