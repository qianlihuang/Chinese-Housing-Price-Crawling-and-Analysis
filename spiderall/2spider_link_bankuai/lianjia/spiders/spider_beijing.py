# spider.py

import scrapy

from lianjia.items import LianjiaItem

import json


class LianjiaSpider(scrapy.Spider):
    name = "lianjia_beijing"
    allowed_domains = ["bj.lianjia.com"]

    with open(
        "../1spider_link_district/lianjia_beijing.json", "r", encoding="utf-8"
    ) as f:
        url_list = []
        for line in f:
            url_list.append(json.loads(line))

    start_urls = []
    for url in url_list:
        url = "https://bj.lianjia.com" + url["link_district"]
        print(url)
        start_urls.append(url)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_delay = 5  # 设置下载延迟,防止被封

    def parse(self, response, **kwargs):
        item = LianjiaItem()

        info_list = response.xpath('//li[@class="filter__item--level3  "]')

        print("info_list:", info_list)
        for info in info_list:
            item["name"] = info.xpath("./a/text()").get()
            item["link_district"] = info.xpath("./a/@href").get()

            yield item
