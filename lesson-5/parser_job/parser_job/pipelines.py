# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class ParserJobPipeline:
    
    def __init__ (self):
        self.db=MongoClient("127.0.0.1:27017")["MvideoParser"];
    
    
    
    def process_item(self, item, spider):
        
        # item is a result of the parsing
        # spider is the information of the parser source
        
        self.db.tvs.insert_one(item);
        
        print("  --> New TV-item {}".format(item))
        return item
