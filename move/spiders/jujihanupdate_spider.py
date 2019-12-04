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

    name="jujihanupdate" #定义蜘蛛名

    def start_requests(self):# 由此方法通过下面链接爬取页面
        allowed_domains=['https://www.juji.tv'];
        #定义爬取的链接
        sql_str = "select href,id,video,update_title,create_time,name from move_meijutt where  is_update=1 and platform in(2,3,4)"
        urls = mysqlDb().query_formatrs(sql_str)

        for url in urls:
            item = MoveItem()
            item['move_id'] = url[1]
            item['video'] = url[2]
            item['update_title'] = url[3]
            item['create_time']=url[4]
            item['name']=url[5]
            yield scrapy.Request(url=item['video'],meta={'item': item},dont_filter=True,callback=self.details,errback=self.errback_httpbin) #11
            print('等待10S')
            #time.sleep(10)  
        #邮件通知

    def errback_httpbin(self, failure):

        self.logger.error(repr(failure))
        self.logger.error(444)
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
                update_title = response.xpath('//dd[text()="备注："]//span//text()')[0].extract()

                item['update_title'] = update_title
                p = re.compile('全')
                findall = p.findall(update_title)
                if findall:
                    item['is_update'] = 0
                else:
                    item['is_update'] = 1
                item['result'] = hrefs[0]

                item['result'] = json.loads(hrefs[0])
                i=1
                item['video_list'] = []
                update=0
                update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                for  each in item['result']['Data']:
                     #线路i
                     title = each['playname']
                     
                     sql_query = " select count(move_id) as move_id from move_move_video where `move_id` ='" +str(item['move_id'])  + "' and  `password`='" + title + "' and `type`="+str(i)
                     
                     sql_data = mysqlDb().query(sql_query)
                     
                     sql_query = " select title from move_move_video where `move_id` ='" +str(item['move_id'])  + "' and  `password`='" + title + "' and `type`="+str(i)+" limit 1"
                     
                     sql_data_title = mysqlDb().query(sql_query)
                    
                     if sql_data_title[0]!=each['playurls'][0][0]:
                        #降序
                        print('降序')
                        number=len(each['playurls'])
                        sort=0
                     else:
                        #升序
                        sort=1
                        number=1
                        print('升序')   
                     # 集数相同就不用更新了
                     if len(each['playurls']) != sql_data[0]:
                            for list in each['playurls']:

                              if number <= sql_data[0]:
                                 if sort:
                                    number += 1
                                    print(list[0])
                                    print('集数已存在')
                                 else:
                                    number -= 1   
                                    print(list[0])
                                    print('集数已存在')
                                 continue
                              else:
                                  print(list[0])
                                  update=1
                                  a = list[1].split('/')
                                  if a[-1] != 'playlist.m3u8':
                                      try:
                                          r=requests.get(list[1])
                                          m3u8 = r.text.split('\n')[2]
                                          url = list[1]
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
                                  if sort:
                                     number += 1
                                  else:
                                     number -= 1
                                  item['video_list'].append(aa)
                                 
                            #print(item)
                            if update==1:
                              
                               #更新主库
                               sql=" update move_meijutt set update_title=%s,is_update=%s,update_time=%s,create_time=%s where id=%s"
                              
                               try:
                                  mysqlDb().execute_update_insert( sql,(item['update_title'],item['is_update'],update_time,item['create_time'],item['move_id']))
                               except Exception as e:
                                  print(e)
                            yield  item
                     else:
                         print('没更新')
                     i += 1
                     
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


