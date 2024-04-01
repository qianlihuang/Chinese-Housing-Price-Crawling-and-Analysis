# spider.py

import scrapy

from lianjia.items import LianjiaItem

import json


class LianjiaSpider(scrapy.Spider):
    name = "lianjia_suzhou"
    allowed_domains = ["su.lianjia.com"]
    # 从1spider_link_district/lianjia_beijing.json中读取url
    # {"name": "东城", "link_district": "/zufang/dongcheng/"}
    # {"name": "西城", "link_district": "/zufang/xicheng/"}

    with open(
        "../1spider_link_district/lianjia_suzhou.json", "r", encoding="utf-8"
    ) as f:
        url_list = []
        for line in f:
            url_list.append(json.loads(line))

    start_urls = []
    for url in url_list:
        url = "https://su.lianjia.com" + url["link_district"]
        print(url)
        start_urls.append(url)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_delay = 5  # 设置下载延迟,防止被封

    def parse(self, response, **kwargs):
        # print(response.body)
        item = LianjiaItem()
        # <li data-id="18335647" data-type="bizcircle" class="filter__item--level3  "><a href="/zufang/andingmen/">安定门</a></li>
        info_list = response.xpath('//li[@class="filter__item--level3  "]')

        print("info_list:", info_list)
        for info in info_list:
            item["name"] = info.xpath("./a/text()").get()
            item["link_district"] = info.xpath("./a/@href").get()

            yield item

        # url = self.url
        # yield scrapy.Request(url, callback=self.parse)
