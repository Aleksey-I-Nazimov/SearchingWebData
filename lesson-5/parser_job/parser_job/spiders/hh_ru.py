import scrapy
from scrapy.http import HtmlResponse
from pprint import pprint
from lxml import html

class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    
    # all domains for parsing:-------------------
    allowed_domains = ['hh.ru']
    
    # staring page:------------------------------
    start_urls = ['https://hh.ru/vacancies/data-scientist?page=0']

    # response is an object of scrappy
    def parse(self, response:HtmlResponse):
        
         # html_page = html.fromstring(response.text)
         # vacansy_serp_result = html_page.get_element_by_id("a11y-main-content")
         #
         # # All vacancy list:-----------------------------------------------------
         # serp_items = vacansy_serp_result.find_class("serp-item")
         #
         # for page_cnt,serp_item in enumerate(serp_items):
         #
         #     # Vacancy info:-----------------------------------------------------
         #     a_tag=serp_item.find_class("serp-item__title")[0]
         #
         #     # Salary info:------------------------------------------------------
         #     salary_tag = serp_item.find_class("bloko-header-section-3");
         #     if len (salary_tag)>1 :
         #         salary_tag = salary_tag[1].text_content()
         #     else :
         #         salary_tag = "not set"
         #
         #     # Vacancy resume:---------------------------------------------------
         #     yield{
         #         'page_cnt': page_cnt,
         #         'name': a_tag.text_content(),
         #         'reference': next(a_tag.iterlinks())[2],
         #         'salary': salary_tag
         #         }
         #
         # #print ("\n++++++\n{}\n++++++++\n".format(response.text))
         pass
        
        
    # 
    # response.follow(url,callback) -> creates subrequest for internal link and
    
