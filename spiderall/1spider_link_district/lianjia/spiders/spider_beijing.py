# spider.py

import scrapy

from lianjia.items import LianjiaItem


class LianjiaSpider(scrapy.Spider):
    name = "lianjia_beijing"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ["https://bj.lianjia.com/zufang/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_delay = 5

    def parse(self, response, **kwargs):
        print(response.body)
        item = LianjiaItem()

        info_list = response.xpath('//li[@data-type="district"]')

        print("info_list:", info_list)
        for info in info_list:
            item["name"] = info.xpath("./a/text()").get()
            item["link_district"] = info.xpath("./a/@href").get()

            yield item

        # url = self.url
        # yield scrapy.Request(url, callback=self.parse)
