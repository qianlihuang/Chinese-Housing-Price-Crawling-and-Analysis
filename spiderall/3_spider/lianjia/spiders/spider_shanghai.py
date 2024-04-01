# spider.py

import scrapy

from lianjia.items import LianjiaItem

import json


class LianjiaSpider(scrapy.Spider):
    name = "lianjia_shanghai"
    allowed_domains = ["sh.lianjia.com"]
    with open(
        "../2spider_link_bankuai/lianjia_shanghai_processed.json", "r", encoding="utf-8"
    ) as f:
        url_list = [json.loads(line) for line in f]

    start_urls = ["https://sh.lianjia.com" + url_list[0]["link_district"]]

    page_index = 1  # 页面计数

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_delay = 5  # 设置下载延迟,防止被封

    def parse(self, response, **kwargs):
        item = LianjiaItem()

        house_total = response.xpath("//span[@class='content__title--hl']/text()").get()
        house_total = int(house_total)
        print("house_total:", house_total)
        page_total = house_total // 30 + 1
        print("page_total:", page_total)

        info_list = response.xpath('//div[@class="content__list--item--main"]')
        for info in info_list:
            item["name"] = info.xpath(
                './p[@class="content__list--item--title"]/a/text()'
            ).get()
            if not item["name"]:
                item["name"] = info.xpath(
                    './p[@class="content__list--item--title twoline"]/a/text()'
                ).get()
            if item["name"]:
                item["name"] = item["name"].strip()
                # print(item["name"])

            item["district"] = info.xpath(
                './p[@class="content__list--item--des"]/a[2]/text()'
            ).get()

            item["total_price"] = info.xpath(
                './span[@class="content__list--item-price"]/em/text()'
            ).get()

            item["area_direction_layout"] = info.xpath(
                './p[@class="content__list--item--des"]/text()'
            ).extract()
            if item["area_direction_layout"]:
                item["area_direction_layout"] = [
                    i.strip() for i in item["area_direction_layout"] if i.strip()
                ]
            yield item

        print("self.page_index:", self.page_index)
        print("page_total:", page_total)

        if self.page_index >= page_total or page_total == 0:
            self.page_index = 0
            self.url_list = self.url_list[1:]

        self.page_index += 1

        if self.url_list:
            url = (
                "https://sh.lianjia.com"
                + self.url_list[0]["link_district"]
                + "pg"
                + str(self.page_index)
            )
            yield scrapy.Request(url, callback=self.parse)
