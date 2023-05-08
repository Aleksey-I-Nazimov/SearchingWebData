# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class WebParserPipeline:

    def __init__ (self):
        self.db=MongoClient("127.0.0.1:27017")["BookShopParser"];
    
    def process_item(self, item, spider):
        
        # item is a result of the parsing
        # spider is the information of the parser source
        
        self.db.books.insert_one(item);
        
        print("  --> New BOOK-item {}".format(item))
        return item


# Special pipeline for images:-----------------------------------------------------------
class BookPhotoPipeline(ImagesPipeline):
    
    def __init__(self, store_uri, download_func=None, settings=None):
        ImagesPipeline.__init__(self, store_uri, download_func=download_func, settings=settings)
    
    def get_media_requests(self, item, info):
        
        img_src = item['img_src']
        
        print ("  --> Processing image {}".format(img_src))
        
        if img_src:
            try:
                yield Request(img_src)
            except Exception as e:
                print("Error {}".format(e))#,logging.CRITICAL)
        