from move.items import MoveItem
import scrapy
import re
import time
import datetime
import MySQLdb
import random
from interval import Interval
from move import settings
import scrapy


class mjw91Spider(scrapy.Spider):
    name = "91mjw"

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        allowed_domains = ["https://91mjw.com"]
        urls = [
            "https://91mjw.com/category/all_mj/dongzuopian",
        ]
        for url in urls:

            yield  scrapy.Request(url=url, meta={'page': url}, dont_filter=True, callback=self.parse)  # 11

        # 邮件通知

    def parse(self, response):
        i = 0
        print(response.xpath('//article[@class="u-movie"]'))

        for each in response.xpath('//article[@class="u-movie"]'):
            # 片名
            name = each.css('a::text').extract_first()
            print(name)
            # 片封面class="bor_img3_right"
            # img = each.xpath("//div[@class='bor_img3_right']//img[@class='list_pic']//@data-original")[i].extract()
            # #片单页url
            # href = each.xpath("//div[@class='bor_img3_right']//@href")[i].extract()
            # #爬取内页数据
            # details_href = response.urljoin(href)
            # item = MoveItem()
            # item['name'] = name
            # item['page'] = response.meta['page']
            # item['img'] = img
            # item['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            # item['href'] = response.urljoin(href)
            # item['onei'] = i
            # i = i + 1
            # time.sleep(3)
