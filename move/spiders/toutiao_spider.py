# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from move.items import toutiaoItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time
from os import path
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
class DfvideospiderSpider(CrawlSpider):
    name = 'toutiao'


    def start_requests(self):  # 由此方法通过下面链接爬取页面
        allowed_domains = ['m.meijutt.com']
        urls = [
            "https://m.meijutt.com/video/770-0-0.html",
        ]
        # rules = (
        #     Rule(LinkExtractor(allow=r'video.eastday.com/a/\d+.html'),
        #          callback='parse_item', follow=True),
        # )

        for url in urls:

            yield scrapy.Request(url=url, meta={'page': url}, dont_filter=True, callback=self.parse_item)  # 11

    def parse_item(self, response):
        filename = '4353%s.html' % 34  # 拼接文件名，如果是第一页，最终文件名便是：mingyan-1.html
        with open(filename, 'wb') as f:  # python文件操作，不多说了；
            f.write(response.body)  # 刚才下载的页面去哪里了？response.body就代表了刚才下载的页面！
        self.log('保存文件: %s' % filename)  # 打个日志
        # item = toutiaoItem()
        # try:
        #     item["video_url"] = response.xpath('//input[@id="mp4Source"]/@value').extract()[0]
        #     item["video_title"] = response.xpath('//meta[@name="description"]/@content').extract()[0]
        #     # print(item)
        #     item["video_url"] = 'http:' + item['video_url']
        #     yield scrapy.Request(url=item['video_url'], meta=item, callback=self.parse_video)
        # except:
        #     pass

    def parse_video(self, response):

        i = response.meta
        file_name = Join()([i['video_title'], '.mp4'])
        base_dir = path.join(path.curdir, 'VideoDownload')
        video_local_path = path.join(base_dir, file_name.replace('?', ''))
        i['video_local_path'] = video_local_path

        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        with open(video_local_path, "wb") as f:
            f.write(response.body)

        yield i