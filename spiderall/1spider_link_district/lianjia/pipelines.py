# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class LianjiaPipeline:
    def open_spider(self, spider):
        if spider.name == "lianjia_beijing":
            self.json_file = open("lianjia_beijing.json", "w", encoding="utf-8")
        elif spider.name == "lianjia_shanghai":
            self.json_file = open("lianjia_shanghai.json", "w", encoding="utf-8")
        elif spider.name == "lianjia_shenzhen":
            self.json_file = open("lianjia_shenzhen.json", "w", encoding="utf-8")
        elif spider.name == "lianjia_guangzhou":
            self.json_file = open("lianjia_guangzhou.json", "w", encoding="utf-8")
        elif spider.name == "lianjia_suzhou":
            self.json_file = open("lianjia_suzhou.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        dict_item = dict(item)

        json_str = json.dumps(dict_item, ensure_ascii=False) + "\n"
        self.json_file.write(json_str)

        return item

    def close_spider(self, spider):
        self.json_file.close()
