from move.items import MoveItem
import scrapy
import re
import time
import datetime
import MySQLdb
import random
from interval import Interval
from move import settings
class meijuba(scrapy.Spider): #需要继承scrapy.Spider类

    name="meijuba" #定义蜘蛛名

    def start_requests(self):# 由此方法通过下面链接爬取页面
        allowed_domains=['http://www.meiju8.cc'];
        #定义爬取的链接
        urls=[
            #"http://www.meiju8.cc/frim/1.html",
            "http://www.meiju8.cc/frim/2_9.html",
            "http://www.meiju8.cc/frim/3.html",
            "http://www.meiju8.cc/frim/4.html",
            "http://www.meiju8.cc/frim/5.html",
            "http://www.meiju8.cc/frim/6.html",
            "http://www.meiju8.cc/frim/7.html",
        ]

        for url in urls:

            yield scrapy.Request(url=url,meta={'page': url},dont_filter=True,callback=self.parse,errback=self.errback_httpbin) #11

        #邮件通知

    def errback_httpbin(self, failure):

        self.logger.error(repr(failure))
        self.logger.error(444)

    def parse(self, response):
        i=0
        for each in response.xpath('//div[@class="cn_box2"]'):
            #片名
            name=each.css('a::text').extract_first()
            #print(name)
            #片封面class="bor_img3_right"
            img = each.xpath("//div[@class='bor_img3_right']//img[@class='list_pic']//@data-original")[i].extract()
            #片单页url
            href = each.xpath("//div[@class='bor_img3_right']//@href")[i].extract()
            #爬取内页数据
            details_href = response.urljoin(href)
            item = MoveItem()
            item['name'] = name
            item['page'] = response.meta['page']
            item['img'] = img
            item['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            item['href'] = response.urljoin(href)
            item['onei'] = i
            i = i + 1
            time.sleep(3)
            yield scrapy.Request(url=details_href,meta={'item': item},dont_filter=True, callback=self.details)

        time.sleep(20)
        #判断是否有下一页
        if response.xpath("//div[@class='list3_cn_box cn2_box_bg']//div[@class='page']//a[last()]/text()").extract() and response.xpath("//div[@class='list3_cn_box cn2_box_bg']//div[@class='page']//a[last()]/text()").extract()[0]=='下一页>>':
            next_page=response.xpath("//div[@class='list3_cn_box cn2_box_bg']//div[@class='page']//a[last()]//@href").extract()[0]
            next_page = response.urljoin(next_page)
            #print('执行下一页'+next_page)
            yield scrapy.Request(next_page,meta={'page': next_page},dont_filter=True, callback=self.parse)
            """
            if next_page!='http://www.meiju8.cc/frim/1-3.html':
                yield scrapy.Request(next_page, callback=self.parse)
                print(next_page)
                pass
             """
        else:
            pass
    # 内页数据处理
    def details(self, response) :

        details_url=response.xpath("//h2[text()='m3u8快播']//../../parent::*/following-sibling::*//@href").extract()
        item = response.meta['item']
        # print('---内页url')
        # print(details_url)
        #print(item['name'] + '---执行内页的数据')
        #print(str(item['onei']) + '---执行列表第几条')
        if not details_url:
            yield []
            pass
        v = 0
        timeArray=''
        for details_urls in details_url:
            #判断该剧有没有更新，没更新就停止   //em[text()='时间：']//parent::li//text()")[1].extract()
            # 最新更新时间
            item['create_time'] = response.xpath("//em[text()='时间：']//parent::li//text()")[1].extract()
            print(item['create_time'])
            timeArray = time.strptime(item['create_time'], "%Y/%m/%d %H:%M:%S")

            print(timeArray)
            print('时间')
            #最后更新时间戳
            timeStamp = int(time.mktime(timeArray))
            #今天时间戳
            today = datetime.date.today()
            # 昨天时间戳
            yesterday = today - datetime.timedelta(days=1)
            # 昨天开始时间戳
            yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
            # 昨天结束时间戳
            yesterday_end_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) - 1
            #判断是否在区间，在就往后执行更新！
            time=Interval(yesterday_start_time,yesterday_end_time)
            #中断返回
            if timeStamp not in time:
                yield []
                pass
            # 内页第几集
            details_title = response.xpath("//h2[text()='m3u8快播']//../../parent::*/following-sibling::*//a/text()")[v].extract()
            #内页url
            item['video'] =response.urljoin(details_urls)
            #介绍
            item['content'] = response.xpath("//ul[@class='omov_list3 font_list3']//p/text()").extract_first()
            #过滤内容
            content=re.search('www.meiju8.cc',item['content'])
            if content:
               item['content']=item['content'].replace("www.meiju8.cc",'')
               pass
            #年份
            try:
               item['year'] = response.xpath('//em[text()="时间："]//parent::li//text()')[3].extract()
               if item['year']=='0':
                  item['year']=2019
            except IndexError:
               item['year']=2019
            # 主演
            try:
                item['actor'] = response.xpath('//em[text()="主演："]//parent::li//text()')[1].extract()
            except IndexError:
                item['actor']=''
            # 导演
            try:
                item['director'] = response.xpath('//em[text()="导演："]//parent::li//text()')[1].extract()
            except IndexError:
                item['director']=''
            #评分
            _minfo=response.css('script:contains("_minfo")::text').get()
            item['score']=re.findall(".*pf\":\"(.*)\",\"pnum.*", _minfo)[0]
            #print('评分',item['score'])
            if item['score']<'1':
                item['score']=round(random.uniform(6,8),1)
            #print('后评分',item['score'])
            #类型
            type=response.xpath('//em[text()="类型："]//parent::li//text()')[1].extract()
            type_split=type.split('/',1)
            item['type']=type_split[1]
            numbers = re.findall(".*第(.*)集.*", details_title)

            if numbers:
                number = numbers[0]
                pass
            else:
                number = 1
                pass
            video_url = response.urljoin(details_urls)
            v = v + 1
            """
            if len(details_url)<3:
                 pass
            elif len(details_url)>3 and len(details_url)<10:
                time.sleep(2)
            else:
                time.sleep(3)
            """
            yield scrapy.Request(video_url, meta={'item': item,'number':number,'details_title':details_title},dont_filter=True, callback=self.get_video)


    #获取资源链接
    def get_video(self,response):

        item = response.meta['item']

        item['details_title']=response.meta['details_title']
        item['number']=response.meta['number']
        playData=response.css('script:contains("playData")::text').get()
        item['status'] =True
        if  playData and  re.findall(".*Url\":\"(.*)\",\"bUrl.*", playData):
            item['result'] = re.findall(".*Url\":\"(.*)\",\"bUrl.*", playData)[0]
            result=item['result'].replace("\\",'')
            item['result']=result
            #判断是否是m3u8文件
            is_true=re.search('.m3u8',item['result'])
            if not is_true:
                item['status'] = False
                item['result'] = False
                pass
            else:
                yield item
            pass
        else :
            item['status'] = False
            item['result'] = False
        #yield item

