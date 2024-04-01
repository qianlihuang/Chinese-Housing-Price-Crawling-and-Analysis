# spider.py

import scrapy

from lianjia.items import LianjiaItem

import json


class LianjiaSpider(scrapy.Spider):
    name = "lianjia_suzhou"
    allowed_domains = ["su.lianjia.com"]
    # 从2spider_link_baikuai/lianjia_beijing.json中读取url
    # {"name": "安定门", "link_district": "/zufang/andingmen/"}
    # {"name": "安贞", "link_district": "/zufang/anzhen1/"}
    with open(
        "../2spider_link_bankuai/lianjia_suzhou_processed.json", "r", encoding="utf-8"
    ) as f:
        url_list = [json.loads(line) for line in f]

    start_urls = ["https://su.lianjia.com" + url_list[0]["link_district"]]

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
                './p[@class="content__list--item--title"]/a/text()'  # {"name": "\n          整租·方丹苑 2室1厅 东北        "}
            ).get()
            if not item["name"]:
                item["name"] = info.xpath(
                    './p[@class="content__list--item--title twoline"]/a/text()'
                ).get()
            if item["name"]:
                item["name"] = item["name"].strip()  # "name": "整租·方丹苑 2室1厅 东北"
                # print(item["name"])

            item["district"] = info.xpath(
                './p[@class="content__list--item--des"]/a[2]/text()'  # "district": "潘家园" # 版块，不是区
            ).get()
            # print(item["district"])

            item["total_price"] = info.xpath(
                './span[@class="content__list--item-price"]/em/text()'  # "total_price": "8200"
            ).get()
            # print(item["total_price"])
            # item["total_price_unit"] = info.xpath(
            #     './span[@class="content__list--item-price"]/text()'
            # ).get()
            # print(item["total_price"], item["total_price_unit"])

            item["area_direction_layout"] = info.xpath(
                './p[@class="content__list--item--des"]/text()'  # "area_direction_layout": ["\n                ", "-", "-", "\n        ", "\n        89.00㎡\n        ", "东北        ", "\n          2室1厅1卫        ", "\n      "]
            ).extract()
            if item["area_direction_layout"]:
                item["area_direction_layout"] = [
                    i.strip() for i in item["area_direction_layout"] if i.strip()
                ]
            # print(item["area_direction_layout"])
            # item["area"] = item["area_direction_layout"][0]
            # item["direction"] = item["area_direction_layout"][1]
            # item["layout"] = item["area_direction_layout"][2]
            # print(item["area"], item["direction"], item["layout"])

            # if (
            #     item["name"]
            #     and item["district"]
            #     and item["total_price"]
            #     and item["total_price_unit"]
            # ):
            #     yield item
            yield item

        print("self.page_index:", self.page_index)
        print("page_total:", page_total)
        # print("url_list:", self.url_list)
        if self.page_index >= page_total or page_total == 0:
            self.page_index = 0  # reset page_index
            self.url_list = self.url_list[1:]  # remove the first url

        self.page_index += 1

        if self.url_list:  # if url_list is not empty
            url = (
                "https://su.lianjia.com"
                + self.url_list[0]["link_district"]
                + "pg"
                + str(self.page_index)
            )
            yield scrapy.Request(url, callback=self.parse)
