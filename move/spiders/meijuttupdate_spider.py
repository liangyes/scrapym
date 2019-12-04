import scrapy
from move.items import MeijuttUpdateItem
from move.common.mysql import mysqlDb
import re
import time
import json
import datetime
import MySQLdb
import random
import requests
from interval import Interval
from move import settings
from urllib.parse import urlparse

#美剧天堂更新
class meijuttupdateSpider(scrapy.Spider):

    name = "meijuttupdate"#定义蜘蛛名

    def start_requests(self):# 由此方法通过下面链接爬取页面
        allowed_domains = ["https://www.meijutt.com"]
        sql_str="select href,id,video,update_title,create_time,name from move_meijutt where is_update=1 and platform=1"
        urls=mysqlDb().query_formatrs(sql_str)
        #print(urls)
        print('查询')
        #exit();
        # urls = [
        #         'http://baidu.com'
        # ]
        for url in urls:
            item = MeijuttUpdateItem()
            item['move_id']=url[1]
            item['video']=url[2]
            item['update_title']=url[3]
            item['create_time']=url[4]
            item['name']=url[5]
            
            yield scrapy.Request(url=url[0],meta={'item': item},dont_filter=True,callback=self.details)
            print('等待10S')
            time.sleep(10)
            
        #邮件通知
    # 内页数据处理
    def details(self,response):
        item = response.meta['item']
        
        #item['is_update'] = response.xpath('//div[@class="o_r_contact"]//font//text()').extract_first()
        create_time = response.xpath("//em[text()='时间：']//parent::label//text()")[1].extract()
        create_time=create_time.replace("/", '-')
        if self.unix_time(create_time)==self.unix_time(str(item['create_time'])):#标题相同 或更新时间相同 不更新
            # 资源没更新
            print(item['name']+'资源没更新')
            yield []
        else:
            href=''
            for each in response.xpath('//div[@class="tabs-list"]'):
                href=each.css('.mn_list_li_movie a::attr(href)').extract_first()
                if href:
                   break
            if href:
                #内页url
                item = response.meta['item']
                item['video'] = response.urljoin(href)
                item['content']=response.css('div.des::text')[0].extract()
                item['content'] = item['content'].replace("'", '')
                item['create_time']=create_time

                #年份des
                try:
                    item['year'] = response.xpath('//em[text()="首播日期："]//parent::li//text()')[1].extract()
                    if item['year'] == '0':
                       item['year'] = 2019
                except IndexError:
                    item['year'] = 2019
                #主演
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
                #print(item)
                yield scrapy.Request(item['video'], meta={'item': item},dont_filter=True, callback=self.get_video)
                #yield item
    # 获取资源链接
    def get_video(self, response):
        item = response.meta['item']
        item['js']=response.css('.ptitle script::attr(src)').extract_first()
        js_url=response.urljoin(item['js'])
        #print(item)
        yield scrapy.Request(js_url, meta={'item': item},
                             dont_filter=True, callback=self.get_js)

        # 获取js内容

    def get_js(self, response):
        item = response.meta['item']
        item['platform'] = 1  # 平台标识 美剧天堂1
        item['score'] = 0  # 目前没评分
        VideoListJson = response.body
        try:
            result = re.findall(".*VideoListJson=(.*),urlinfo.*", VideoListJson.decode('utf-8'))[0]
        except Exception as e:
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            mysqlDb().execute_update_insert(
                "insert into move_error (`name`, platform, error,line,file,`url`,create_time) value(%s, %s, %s, %s, %s, %s, %s)",
                ('获取js内容异常', '美剧天堂', e, '150行',
                 'meijutt', item['js'], create_time))
            print('异常')
            print(response.url)
        item['result'] = result
        item['platform'] = 1
        res = urlparse(response.url)
        path = res.netloc + res.path
        # print(path)
        id = path[-4:-3]  # 获取更新加减id  云播url会更新  更新规则是id的最后一位  ，加或减url的倒数第五位数
        item['result'] = json.loads(item['result'])
        
        for res in item['result']:
            update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            update = 0;  # 更新标识，如果有更新主库
            # 1云播，2云播二，3百度网盘
            if res[0] == '云播':
                i = 1
                item['video_list'] = []
                #先判断已经存了多少集
                sql_query = " select count(move_id) as move_id from move_move_video where `move_id` ='" + str(item['move_id']) + "' and  `type`=1"
                sql_data = mysqlDb().query(sql_query)

                #集数相同就不用更新了
                if  len(res[1])!=sql_data[0]:
                    for a in res[1]:
                        if i<=sql_data[0]:
                           i += 1
                           print(i)
                           print('集数已存在')
                           continue
                        # 判断是否是m3u8文件
                        # print(res[1][0:-5])
                        # print(res[1][-5:-4])
                        # print(res[1][-4:])
                        update=1#有更新
                        resUrl = a[1][0:-5] + a[1][-4:]
                        item['number'] = i  # 集数
                        item['title'] = a[0]  # 标题
                        item['type'] = 1  # 云播
                        i += 1
                        # 获取二层m3u8 地址
                        # time.sleep(2)
                        r = requests.get(resUrl)
                        # time.sleep(3)
                        if r:
                            hrefs = re.findall(".*main = \"(.*)\";.*", r.text)
                            if hrefs:
                                href = hrefs[0]
                                # 获取到地址
                                res = urlparse(resUrl)
                                url = res.scheme + '://' + res.netloc + href
                                # time.sleep(2)
                                r = requests.get(url)
                                # time.sleep(3)
                                if r:
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
                                        ('视频异常:云播二层m3u8链接无效', '美剧天堂:' + item['name'], a[0], '227行',
                                         item['video'], url, create_time))
                            else:
                                m3u8 = ''
                                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                mysqlDb().execute_update_insert(
                                    "insert into move_error (`name`, platform, error,line,file,`url`,create_time) value(%s, %s, %s, %s, %s, %s, %s)",
                                    ('视频异常:云播一层m3u8链接无效', '美剧天堂:' + item['name'], a[0], '246行',
                                     item['video'], resUrl, create_time))
                        else:
                            m3u8 = ''
                            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            mysqlDb().execute_update_insert(
                                "insert into move_error (`name`, platform, error,line,file,`url`,create_time) value(%s, %s, %s, %s, %s, %s, %s)",
                                ('视频异常:云播一层m3u8链接无效', '美剧天堂:' + item['name'], a[0], '227行',
                                 item['video'], resUrl, create_time))
                        aa = [
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
                    #print(item)
                    if update==1:
                        #更新主库
                        sql=" update move_meijutt set update_title=%s,is_update=%s,update_time=%s,create_time=%s where id=%s"
                        mysqlDb().execute_update_insert( sql,(item['update_title'],item['is_update'],update_time,item['create_time'],item['move_id']))
                    yield item
            if res[0] == '云播二':
                sql_query = " select count(move_id) as move_id from move_move_video where `move_id` ='" + str(item[
                    'move_id']) + "' and  `type`=2"
                sql_data = mysqlDb().query(sql_query)
                # 集数相同就不用更新了
                if  len(res[1]) != sql_data[0]:
                    i = 1
                    item['video_list'] = []
                    for a in res[1]:
                        if i <= sql_data[0]:
                            i += 1
                            print(i)
                            print('集数已存在')
                            continue
                        # 判断是否是m3u8文件
                        update=1
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

                    # print(item)
                    if update == 1:
                        # 更新主库
                        sql=" update move_meijutt set update_title=%s,is_update=%s,update_time=%s,create_time=%s where id=%s"
                        mysqlDb().execute_update_insert( sql,(item['update_title'],item['is_update'],update_time,item['create_time'],item['move_id']))
                    yield item
            if res[0] == '百度网盘':
                sql_query = " select count(move_id) as move_id from move_move_video where `move_id` ='" + str(item[
                    'move_id']) + "' and  `type`=3"
                sql_data = mysqlDb().query(sql_query)
                # 集数相同就不用更新了
                if len(res[1]) != sql_data[0]:
                    i = 1
                    item['video_list'] = []
                    for a in res[1]:
                        if i <= sql_data[0]:
                            i += 1
                            print(i)
                            print('集数已存在')
                            continue
                        update=1
                        password = a[1].split('|', 1)
                        # 判断是否有密码
                        if len(password) == 1:
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
                    if update == 1:
                        # 更新主库
                        sql=" update move_meijutt set update_title=%s,is_update=%s,update_time=%s,create_time=%s where id=%s"
                        mysqlDb().execute_update_insert( sql,(item['update_title'],item['is_update'],update_time,item['create_time'],item['move_id']))
                    yield item

    # dt 时间                
    def unix_time(self,dt):
        # 转换成时间数组
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        # 转换成时间戳
        timestamp = int(time.mktime(timeArray))
        return timestamp
