# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ParserJobPipeline:
    def process_item(self, item, spider):
        
        # item is a result of the parsing
        # spider is the information of the parser source
        
        print("New item {}".format(item))
        
        return item
