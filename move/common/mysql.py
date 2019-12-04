import move
import MySQLdb
from move import settings
class mysqlDb():
    def __init__(self):
        '''类例化，处理一些连接操作'''
        # self.host = settings.MYSQL_HOST
        # self.username =  settings.MYSQL_USER
        # self.password = settings.MYSQL_PASSWD
        # self.database = settings.MYSQL_DBNAME
        # self.port = settings.MYSQL_PORT
        self.cur = None
        self.con = None
        # connect to mysql
        try:
            self.con =MySQLdb.connect(host=settings.MYSQL_HOST, db=settings.MYSQL_DBNAME,
                                       user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWD,
                                       charset='utf8', use_unicode=True)
            self.cur = self.con.cursor()
        except:
            pass

    def query_formatrs(self, sql_str):

        '''查询数据，返回一个列表，里面的每一行是一个字典，带字段名
            cursor 为连接光标
            sql_str为查询语句
        '''
        try:
            self.cur.execute(sql_str)
            rows = self.cur.fetchall()
            # r = []
            # for x in rows:
            #     r.append(dict(zip(self.cur.column_names, x)))
            return rows
        except  Exception as e:
            print(e)
            return False
    def query(self,sql_str):
        '''查询数据并返回
                     cursor 为连接光标
                     sql_str为查询语句
        '''
        try:
            self.cur.execute(sql_str)
            rows = self.cur.fetchone()
            return rows
        except:
            return False

    def execute_update_insert(self, sql, _param):

        '''
        插入或更新记录 成功返回最后的id
        '''
        self.cur.execute(sql,_param)
        self.con.commit()
        return self.cur.lastrowid
    def execute_update_insertall(self,  sql,_param):
        try:
            '''
            批量插入
            sql 是一个数组
           
            '''
            rows=self.cur.executemany(sql,_param)
            self.con.commit()
            return  rows
        except:
            return False


    def close(self):
        '''结束查询和关闭连接'''
        self.con.close()




