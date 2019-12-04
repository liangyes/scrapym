from move.items import MoveItem
import scrapy
import re
import time
import datetime
import MySQLdb
import random
import json
import requests
from interval import Interval
from move import settings
from urllib.parse import urlparse
from move.common.mysql import mysqlDb
class meijuba(scrapy.Spider): #需要继承scrapy.Spider类

    name="jujihan" #定义蜘蛛名

    def start_requests(self):# 由此方法通过下面链接爬取页面
        allowed_domains=['https://www.juji.tv'];
        #定义爬取的链接
        urls=[
            "https://www.juji.tv/dianshiju",#韩剧
            "https://www.juji.tv/dianying",#电影
            "https://www.juji.tv/zongyi",#综艺
            "https://www.juji.tv/riju/",#日剧
            "https://www.juji.tv/ribendianying/",#日剧电影
            "https://www.juji.tv/taiju/",#泰剧
            "https://www.juji.tv/taiguodianying/",#泰剧电影
        ]

        for url in urls:

            yield scrapy.Request(url=url,meta={'page': url},dont_filter=True,callback=self.parse,errback=self.errback_httpbin) #11

        #邮件通知

    def errback_httpbin(self, failure):

        self.logger.error(repr(failure))
        self.logger.error(444)

    def parse(self, response):
        i=0
        for each in response.xpath('//ul[@id="contents"]//li'):
            try:
                item = MoveItem()
                #片名
                name= each.xpath('//h5//a//text()')[i].extract()

                #片封面class="bor_img3_right"
                img = each.xpath("//a//img//@src")[i].extract()

                #片单页url
                href = each.xpath("//a[@class='play-img']//@href")[i].extract()

                try:
                   actor = each.xpath('//ul[@id="contents"]//li['+str(i+1)+']//p[1]//text()').extract()[1]
                except:
                   actor=''
                try:
                   type = each.xpath('//ul[@id="contents"]//li['+str(i+1)+']//p[2]//text()').extract()[1]
                except:
                    type='剧情'
                try:
                   content = each.xpath('//ul[@id="contents"]//li['+str(i+1)+']//p[4]//text()').extract()[1]
                except:
                    content=''
                update_title =each.xpath('//ul[@id="contents"]//li['+str(i+1)+']//p[5]//text()').extract()[1]
                p = re.compile('全')
                findall=p.findall(update_title)
                if findall:
                   item['is_update']=0
                else:
                   item['is_update']=1

                #爬取内页数据
                item['name'] = name
                item['img'] = img
                item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                item['href'] = response.urljoin(href)
                hrefType = item['href'].split('/')
                if hrefType[3] in ['dianying','ribendianying','taiguodianying']:
                   item['is_update'] = 0
                   type = '电影'
                if hrefType[3] == 'zongyi':
                   type = '综艺'
                item['video']=item['href']
                item['type'] = type
                item['content'] = content
                item['update_title'] = update_title
                item['actor'] = actor
                item['score'] = '0'
                item['platform'] = 2 #韩剧
                if  hrefType[3] in ['riju','ribendianying']:
                    item['platform'] = 3  # 日剧
                if hrefType[3] in ['taiju','taiguodianying']:
                    item['platform'] = 4  # 泰剧
                i = i + 1
                # 如果存在跳过
                sql_query = " select id from move_meijutt where `name` ='" + item['name'] + "' and  `href`='" + item[
                    'href'] + "'"
                sql_data = mysqlDb().query(sql_query)
                if not sql_data:
                    time.sleep(10)
                    yield scrapy.Request(url=item['href'],meta={'item': item},dont_filter=True, callback=self.details)
                else:
                    print(item['name'] + '已存在')
            except:
                i = i + 1
                continue

        time.sleep(30)
        #判断是否有下一页
        if response.xpath('//a[text()="下一页"]//@href').extract():
            next_page=response.xpath('//a[text()="下一页"]//@href').extract()[0]
            data=response.xpath('//a[text()="下一页"]//@data').extract()[0]
            nextNumber=data.split('-')
            if  nextNumber[1]<'5':
                next_page = response.urljoin(next_page)
                print('执行下一页'+next_page)
                yield scrapy.Request(next_page,meta={'page': next_page},dont_filter=True, callback=self.parse)
            else:
                print(nextNumber[1])
                print('结束')
        else:
            print('结束')

            pass
    # 内页数据处理
    def details(self, response) :
        item = response.meta['item']
        try:
            #获取线路任意一条路径
            href=response.xpath('//ul[@class="play-list"]//li//a//@href')[0].extract()
            a = href.split('/')
            b = a[3].split('-')
            one = b[0] + '-' + b[1]
            two = '-0-1.js'
            a[3] = one + two
            href='/'.join(a)  #js路径
            js_url = response.urljoin(href)
            r = requests.get(js_url)
            hrefs = re.findall(".*ff_urls='(.*)';.*", r.text)

            if hrefs:
                #添加到主库
                year = response.xpath('//dd[text()="年份："]//span//text()')[0].extract()
                director = response.xpath('//dd[text()="导演："]//span//text()')[0].extract()
                item['year'] = year
                item['director'] = director
                item['result'] = hrefs[0]
                #print(item)
                item['move_id'] = mysqlDb().execute_update_insert(
                    "insert into move_meijutt (`name`, href, img,video,content,create_time,`year`,director,actor,score,`type`,result,platform,is_update,update_title) value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (item['name'], item['href'], item['img'], item['video'], '"' + item['content'] + '"',
                     item['create_time'], item['year'], item['director'], item['actor'], item['score'], item['type'],
                     item['result'], item['platform'], item['is_update'], item['update_title']))

                item['result'] = json.loads(hrefs[0])
                i=1
                item['video_list'] = []
                for  each in item['result']['Data']:
                     #线路i
                     number=1
                     #标题  更新的唯一标识
                     title=each['playname']
                     for list in each['playurls']:
                          #判断链接是否完整
                          a = list[1].split('/')
                          if a[-1]!='playlist.m3u8':
                             try:
                                 r=requests.get(list[1])
                                 m3u8 = r.text.split('\n')[2]
                                 url=list[1]
                                 res = urlparse(url)
                                 # 个别链接不拼接path
                                 split = m3u8.split('/')
                                 if split[0]:
                                     url = res.scheme + '://' + res.netloc + res.path
                                     list[1] = list[1][0: -10] + m3u8
                                     print('100Kurl')
                                     print(list[1])

                                 else:
                                     url = res.scheme + '://' + res.netloc
                                     list[1] = url + m3u8
                                     print('另外')
                                     print(url)
                                     print(list[1])
                             except:
                                  print('异常！')

                          aa = [
                             item['move_id'],
                             item['name'],
                             list[0],
                             list[1],
                             title,
                             time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                             number,
                             i,
                          ]
                          number+=1
                          item['video_list'].append(aa)
                     i += 1
                     pass

                yield  item
            else:
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                mysqlDb().execute_update_insert(
                    "insert into move_error (`name`, platform, error,line,file,`url`,create_time) value(%s, %s, %s, %s, %s, %s, %s)",
                    ('韩剧新增异常:'+item['name'], '韩剧新增异常', js_url, '154行',
                     '韩剧', response.url, create_time))
        except Exception as e :
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            mysqlDb().execute_update_insert(
                "insert into move_error (`name`, platform, error,line,file,`url`,create_time) value(%s, %s, %s, %s, %s, %s, %s)",
                ('韩剧新增异常:'+item['name'], '韩剧新增异常', e, '160行',
                 '韩剧', response.url, create_time))


