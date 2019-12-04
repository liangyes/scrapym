# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from move.common.mysql import mysqlDb
import time
import pymongo
import json
from move import settings
class MovePipeline(object):
    #mysql写入
    def __init__(self):
        # mysql写入
        self.connect = ''
        self.cursor = ''
        try:
            self.connect = MySQLdb.connect(host=settings.MYSQL_HOST, db=settings.MYSQL_DBNAME,
                                           user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWD,
                                           charset='utf8', use_unicode=True)
        except Exception as error:
            print(error)
        self.cursor = self.connect.cursor();
    def process_item(self, item, spider):
        print('第一组件')
        if  spider.name=='meijuba':
            try:
                #主库
                #先查询数据是否存在
                checksql=" select * from move_meijuba where `name` ='"+item['name']+"'"
                print(checksql)
                fetchone=self.cursor.execute(checksql)
                if fetchone:
                    move_id = self.cursor.fetchone()[0]
                    print(move_id)
                    print('更新')
                    updatesql=" update  move_meijuba set `href`='"+item['href']+"',`img`='"+item['img']+"',`video`='"+item['video']+"',`content`='"+item['content']+"',`create_time`='"+item['create_time']+"',`year`='"+item['year']+"',`director`='"+item['director']+"',`actor`='"+item['actor']+"',`score`='"+item['score']+"',`type`='"+item['type']+"' where  `name`='"+item['name']+"'"
                    print(updatesql)
                    print('\n')
                    self.cursor.execute(updatesql)
                    self.connect.commit()

                else :
                   self.cursor.execute(
                    "insert into move_meijuba (`name`, href, img,video,content,create_time,`year`,director,actor,score,`type`) value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(item['name'], item['href'],item['img'],item['video'],item['content'],item['create_time'],item['year'],item['director'],item['actor'],item['score'],item['type']))
                   self.connect.commit()

                   sql = ''' select LAST_INSERT_ID() '''
                   num = self.cursor.execute(sql)
                   if num > 0:
                       move_id=self.cursor.fetchone()[0]
                print(move_id)
                #资源库
                self.cursor.execute(" insert into move_move_video (`name`, move_id, url,`number`,create_time) value(%s, %s, %s, %s, %s)",(item['details_title'],move_id,item['result'],item['number'],item['create_time']))
                print('\n')
                self.connect.commit()
            except Exception as error:
            #logging.log(error)
                   print(error)
                   print('\n')
                   return item
        if  spider.name=='meijutt':
            try:
                print('视频插入美剧')
                insert = self.cursor.executemany(
                    " insert into move_move_video (move_id,`name`, title,url,password,create_time,`number`,`type`) value(%s, %s, %s, %s, %s, %s, %s, %s)",
                    item['video_list'])
                if insert:
                    print('视频插入成功！')
                else:
                    print('视频插入异常！')
                self.connect.commit()
            except Exception as error:
                print(error)
                print('\n')
        #meijuttupdate 更新
        if  spider.name == 'meijuttupdate':
            try:
                print('视频插入美剧更新')
                insert = self.cursor.executemany(
                    " insert into move_move_video (move_id,`name`, title,url,password,create_time,`number`,`type`) value(%s, %s, %s, %s, %s, %s, %s, %s)",
                    item['video_list'])
                if insert:
                    print('视频插入成功！')
                else:
                    print('视频插入异常！')
                self.connect.commit()
            except Exception as error:
                print(error)
                print('\n')
        #韩剧新增
        if  spider.name=='jujihan':
            try:
                print('视频插入韩剧新增')
                insert = self.cursor.executemany(
                    " insert into move_move_video (move_id,`name`, title,url,password,create_time,`number`,`type`) value(%s, %s, %s, %s, %s, %s, %s, %s)",
                    item['video_list'])
                if insert:
                    print('韩剧视频插入成功！')
                else:
                    print('韩剧视频插入异常！')
                self.connect.commit()
            except Exception as error:
                print(error)
                print('\n')
        #jujihanupdate韩剧更新
        if  spider.name == 'jujihanupdate':
            try:
                print('视频插入韩剧更新')
                insert = self.cursor.executemany(
                    " insert into move_move_video (move_id,`name`, title,url,password,create_time,`number`,`type`) value(%s, %s, %s, %s, %s, %s, %s, %s)",
                    item['video_list'])
                if insert:
                    print('视频插入成功！')
                else:
                    print('视频插入异常！')
                self.connect.commit()
            except Exception as error:
                print(error)
                print('\n')
    def close_spider(self, spider):
        self.connect.close();
class MeijuttPipeline(object):
    #mysql写入
    def __init__(self):
        self.connect=''
        self.cursor=''
        try:
           self.connect = MySQLdb.connect(host=settings.MYSQL_HOST, db=settings.MYSQL_DBNAME,
                                       user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWD,
                                       charset='utf8', use_unicode=True)
        except Exception as error:
               print(error)
        self.cursor = self.connect.cursor();
    def process_item(self, item, spider):
        print('meijutt' + '新增入口aaaa')
        if spider.name!='meijutt':
           exit()
        try:
            print('视频插入')
            insert=self.cursor.executemany(
                " insert into move_move_video (move_id,`name`, title,url,password,create_time,`number`,`type`) value(%s, %s, %s, %s, %s, %s, %s, %s)",
                item['video_list'])
            if insert:
               print('视频插入成功！')
            else:
               print('视频插入异常！')
            self.connect.commit()
        except Exception as error:
               print(error)
               print('\n')
    def close_spider(self, spider):  self.connect.close();
