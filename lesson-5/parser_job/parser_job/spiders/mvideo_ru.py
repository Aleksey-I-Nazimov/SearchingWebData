import scrapy
from datetime import datetime

class MvideoRuSpider(scrapy.Spider):
    
    name = 'mvideo_ru'
    
    allowed_domains = ['mvideo.ru']
    
    start_urls = ['https://www.mvideo.ru/televizory-i-cifrovoe-tv-1/televizory-65/f/tolko-v-nalichii=da']

    def parse(self, response):
        
        next_page = response.xpath("//a[contains(@class,'page-link icon ng-star-inserted')]/@href");#[0].text_content();#.get();
        print(next_page)
        #yield response.follow(next_page,callback=self.parse)
        
        tv_list = response.xpath("//div[contains(@class,'product-cards-layout__item')]").getall();
        for tv in tv_list:
            model_name = tv.xpath("//div[contains(@class,'product-title product-title--list')]/a")[0].text_content()
            model_price = tv.xpath("//span[contains(@class,'price__main-value')]")[0].text_content();
            yield {
                'model':model_name,
                'price':model_price,
                'date':str(datetime.now())
                }
        
