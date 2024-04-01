# spider.py

import scrapy

from lianjia.items import LianjiaItem


class LianjiaSpider(scrapy.Spider):
    name = "lianjia_suzhou"
    allowed_domains = ["su.lianjia.com"]
    start_urls = ["https://su.lianjia.com/zufang/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_delay = 5  # 设置下载延迟,防止被封

    def parse(self, response, **kwargs):
        print(response.body)
        item = LianjiaItem()
        # print("item:", item)
        # <li data-id="23008614" data-type="district" class="filter__item--level2  "> <a href="/zufang/dongcheng/">东城</a> </li>
        info_list = response.xpath('//li[@data-type="district"]')

        print("info_list:", info_list)
        for info in info_list:
            item["name"] = info.xpath("./a/text()").get()
            item["link_district"] = info.xpath("./a/@href").get()

            yield item

        # url = self.url
        # yield scrapy.Request(url, callback=self.parse)
