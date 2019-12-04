from move.items import MeijuttItem
import scrapy
import re
import time
import json
import datetime
import win32api
import MySQLdb
import random
import requests
from interval import Interval
from move import settings
from urllib.parse import urlparse
from move.common.mysql import mysqlDb
class meijuttSpider(scrapy.Spider):

    name = "meijutt"#定义蜘蛛名

    def start_requests(self):# 由此方法通过下面链接爬取页面
        allowed_domains = ["https://www.meijutt.com"]
        urls = [
            "https://www.meijutt.com/file/list1.html",#魔幻/科幻
            "https://www.meijutt.com/file/list2.html",#灵异/惊悚
            "https://www.meijutt.com/file/list3.html",#都市/情感
            "https://www.meijutt.com/file/list4.html",#犯罪/历史
            "https://www.meijutt.com/file/list5.html",#选秀/综艺
            "https://www.meijutt.com/file/list6.html",#动漫/卡通
        ]
       
        for url in urls:
            print(url)
            yield scrapy.Request(url=url,meta={'page': url},dont_filter=True,callback=self.parse)
            #time.sleep(600)
        #邮件通知

    def parse(self, response):
        i = 0
        for each in response.xpath('//div[@class="cn_box2"]'):
            name= each.css('a::text').extract_first()#标题
            img = each.xpath("//div[@class='bor_img3_right']//img[@class='list_pic']//@src")[i].extract()#封面
            href = each.xpath("//div[@class='bor_img3_right']//@href")[i].extract()
            # 爬取内页数据
            details_href = response.urljoin(href)
            item = MeijuttItem()
            item['name'] = name
            #item['page'] = response.meta['page']
            item['img'] = img
            item['href'] = response.urljoin(href)
            print('查询是否存在')    
            #判断是否已经存在数据库
            sql_query = " select id from move_meijutt where `name` ='" + item['name'] + "' and  `href`='" + item[
                'href'] + "'"
            sql_data = mysqlDb().query(sql_query)
            i = i + 1
            if  not sql_data:
                print('不存在')
                time.sleep(3)
                yield scrapy.Request(url=details_href, meta={'item': item}, dont_filter=True, callback=self.details)
            else:

                print(item['name']+'已存在')
                yield []

        time.sleep(30)
        # #判断是否有下一页
        if  response.xpath('//div[@class="page"]//a[text()="下一页"]//@href').extract():
            next_page=response.xpath('//div[@class="page"]//a[text()="下一页"]//@href').extract()[0]
            #判断是否是前三页
            # next_page=response.urljoin(next_page)
            # yield scrapy.Request(url=next_page,dont_filter=True,callback=self.parse)
            b=next_page.split('_');
            if b[1][:1]<'4':    
                next_page=response.urljoin(next_page)
                yield scrapy.Request(url=next_page,dont_filter=True,callback=self.parse)
                print('下一页')
                print(next_page)
            else:
                print(next_page+'分类结束')    
    # 内页数据处理
    def details(self,response):
        list=response.css(".tabs-list").extract()
        href=''
        for each in response.xpath('//div[@class="tabs-list"]'):
            href=each.css('.mn_list_li_movie a::attr(href)').extract_first()
            #print(href)
            if href:
               break
        if href:
            #print(href)
            # 内页url
            item = response.meta['item']
            item['video'] = response.urljoin(href)
            item['content']=response.css('div.des::text')[0].extract()
            item['content'] = item['content'].replace("'", '')

            # 年份des
            try:
                item['year'] = response.xpath('//em[text()="首播日期："]//parent::li//text()')[1].extract()
                if item['year'] == '0':
                    item['year'] = 2019
            except IndexError:
                item['year'] = 2019
            # 主演
            try:
                item['actor'] = response.xpath('//em[text()="主演："]//parent::li//text()')[1].extract()
                if item['actor']=='更多>>':
                   item['actor']=''
            except IndexError:
                item['actor'] = ''
            # 导演
            try:
                item['director'] = response.xpath('//em[text()="导演："]//parent::li//text()')[1].extract()
                if item['director'] == '更多>>':
                    item['director'] = ''
            except IndexError:
                item['director'] = ''
            #类型
            try:
                type = response.xpath('//em[text()="类型："]//parent::span//text()')[1].extract()
                if type == '更多>>':
                   type = '科幻'
                item['type'] = type.split('/')[0]
            except IndexError:
                item['type'] = '科幻'
            # 是否还更新
            item['is_update']=response.xpath('//div[@class="o_r_contact"]//font//text()').extract_first()
            #更新至第几集
            item['update_title']=item['is_update']
            if item['is_update'] in ['全剧完结','本季终']:
               item['is_update']=0
            else:
               item['is_update']=1
            #print(item['is_update'])
            item['create_time'] = response.xpath("//em[text()='时间：']//parent::label//text()")[1].extract()

            yield scrapy.Request(item['video'], meta={'item': item},
                                 dont_filter=True, callback=self.get_video)
        else:
            #资源没更新
            item = response.meta['item']
            print(item['name'])
            print('资源没更新')
            yield []
            #yield item
    # 获取资源链接
    def get_video(self, response):
        item = response.meta['item']
        item['js']=response.css('.ptitle script::attr(src)').extract_first()
        item['js']=response.urljoin(item['js'])
        #print(item)
        yield scrapy.Request( item['js'], meta={'item': item},
                             dont_filter=True, callback=self.get_js)

    # 获取js内容
    def get_js(self,response):
        item = response.meta['item']
        item['platform'] = 1  #平台标识 美剧天堂1
        item['score'] = 0  # 目前没评分
        VideoListJson=response.body
        try:
           result = re.findall(".*VideoListJson=(.*),urlinfo.*", VideoListJson.decode('utf-8'))[0]
        except Exception as e:
               create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
               mysqlDb().execute_update_insert(
                  "insert into move_error (`name`, platform, error,line,file,`url`,create_time) value(%s, %s, %s, %s, %s, %s, %s)",
                ('获取js内容异常', '美剧天堂',e, '150行',
                 'meijutt', item['js'], create_time))
               print('异常')
               print(response.url)
               yield []
        item['result']=result
        item['platform']=1
        res = urlparse(response.url)
        path = res.netloc + res.path
        #print(path)
        id=path[-4:-3] #获取更新加减id  云播url会更新  更新规则是id的最后一位  ，加或减url的倒数第五位数
        #print(id)
        #判断数据库是否存在
        sql_query=" select id from move_meijutt where `name` ='" + item['name'] + "' and  `href`='"+item['href']+"'"
        sql_data = mysqlDb().query(sql_query)
        if sql_data:
            move_id=sql_data[0]
        else:
            move_id = mysqlDb().execute_update_insert(
                     "insert into move_meijutt (`name`, href, img,video,content,create_time,`year`,director,actor,score,`type`,result,platform,is_update,update_title) value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(item['name'], item['href'],item['img'],item['video'],'"'+item['content']+'"',item['create_time'],item['year'],item['director'],item['actor'],item['score'],item['type'],item['result'],item['platform'],item['is_update'],item['update_title']))
            print('新增打印sql')
            yield []
        if not move_id :
               create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
               mysqlDb().execute_update_insert(
                   "insert into move_error (`name`, platform, error,line,file,`url`,create_time) value(%s, %s, %s, %s, %s, %s, %s)",
                   ('新增异常','新增异常', '新增异常', '172行',
                    '美剧天堂', 'meijutt',create_time))
               print('打印异常')
               yield []
               pass
        item['move_id']=move_id
        item['result'] = json.loads(item['result'])
        for res in item['result']:
            #print('循环')
            #1云播，2云播二，3百度网盘
            if res[0] == '云播':
                i = 1
                item['video_list'] = []

                for a in res[1]:
                    print('云播')
                    # 判断是否是m3u8文件
                    #print(res[1][0:-5])
                    #print(res[1][-5:-4])
                    #print(res[1][-4:])
                    resUrl=a[1][0:-5]+a[1][-4:]
                    item['number']=i  #集数
                    item['title']=a[0]  #标题
                    item['type']=1  #云播
                    i += 1
                    #获取二层m3u8 地址
                    #time.sleep(2)
                    r = requests.get(resUrl)
                    #time.sleep(3)
                    if r:
                        hrefs = re.findall(".*main = \"(.*)\";.*", r.text)
                        if hrefs:
                            href=hrefs[0]
                            #获取到地址
                            res=urlparse(resUrl)
                            url = res.scheme + '://' + res.netloc + href
                            #time.sleep(2)
                            r = requests.get(url)
                            #time.sleep(3)
                            if  r:
                                m3u8 = r.text.split('\n')[2]
                                res = urlparse(url)
                                # 个别链接不拼接path
                                split = m3u8.split('/')
                                if split[0]:
                                    url = res.scheme + '://' + res.netloc + res.path
                                    m3u8 = url[0: -10] + m3u8
                                    print('100Kurl')
                                    print(m3u8)

                                else:
                                    url = res.scheme + '://' + res.netloc
                                    m3u8 = url + m3u8
                                    print('另外')
                                    print(url)
                                    print(m3u8)
                            else:
                                res = urlparse(url)
                                urls = res.scheme + '://' + res.netloc + res.path
                                m3u8 = urls[0: -10] + '1000k/hls/index.m3u8'
                                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                mysqlDb().execute_update_insert(
                                    "insert into move_error (`name`, platform, error,line,file,`url`,create_time) value(%s, %s, %s, %s, %s, %s, %s)",
                                    ('视频异常:云播二层m3u8链接无效', '美剧天堂:'+item['name'], a[0], '227行',
                                     item['video'], url, create_time))
                        else:
                            m3u8 = ''
                            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            mysqlDb().execute_update_insert(
                                "insert into move_error (`name`, platform, error,line,file,`url`,create_time) value(%s, %s, %s, %s, %s, %s, %s)",
                                ('视频异常:云播一层m3u8链接无效', '美剧天堂:' + item['name'], a[0], '246行',
                                 item['video'], resUrl, create_time))
                    else:
                        m3u8=''
                        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        mysqlDb().execute_update_insert(
                            "insert into move_error (`name`, platform, error,line,file,`url`,create_time) value(%s, %s, %s, %s, %s, %s, %s)",
                            ('视频异常:云播一层m3u8链接无效', '美剧天堂:'+item['name'], a[0], '227行',
                             item['video'], resUrl, create_time))
                    aa=[
                        item['move_id'],
                        item['name'],
                        item['title'],
                        m3u8,
                        '',
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        item['number'],
                        item['type'],
                    ]
                    item['video_list'].append(aa)
                    # print(item)
                yield item
                    #yield scrapy.Request(resUrl, meta={'item': item},dont_filter=True, callback=self.get_m3u8)
            if res[0] == '云播二':
                print('云播二')
                i = 1
                item['video_list'] = []
                for a in res[1]:
                    # 判断是否是m3u8文件
                    m3u8 = a[1].split('m3u8', 1)
                    if len(m3u8) == 2:
                        a[1] = a[1][0:-5] + 'm3u8'
                    aa = [
                        item['move_id'],
                        item['name'],
                        a[0],
                        a[1],
                        '',
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        i,
                        2
                    ]
                    item['video_list'].append(aa)
                    i += 1
                #print(item)
                yield item
            if res[0] == '百度网盘':
                #print('百度网盘')
                i = 1
                item['video_list']=[]
                for a in res[1]:
                    password = a[1].split('|', 1)
                    #判断是否有密码
                    if len(password)==1:
                       password.append('')
                    aa = [
                        item['move_id'],
                        item['name'],
                        a[0],
                        password[0],
                        password[1][1:],
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        i,
                        3
                    ]
                    i += 1
                    item['video_list'].append(aa)
                #print(item)
                yield item
