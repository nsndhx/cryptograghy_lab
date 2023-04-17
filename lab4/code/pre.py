import pymysql
import re
import hashlib
from random import randint

class DataBaseInfo:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'gpc'
        self.password = 'gpc'
        self.dbname = 'test'


    def _connect(self):
        '''连接MySQL数据库'''
        try:
            db = pymysql.connect(
                host=self.host,
                port=3306,
                user=self.user,
                passwd=self.password,
                db='c3server_v3',
                charset='utf8'
                )
            return db
        except Exception:
            raise Exception("数据库连接失败")
        

    def connect(self):
        '''连接MySQL数据库'''
        try:
            db = pymysql.connect(
                host=self.host,
                port=3306,
                user=self.user,
                passwd=self.password,
                db=self.dbname,
                charset='utf8'
                )
            return db
        except Exception:
            raise Exception("数据库连接失败")


    def table_exists(self,table_name):        #这个函数用来判断表是否存在
        db = self._connect()
        cursor = db.cursor()
        sql = "show tables;"
        cursor.execute(sql)
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]
        if table_name in table_list:
            db.close()
            return 1        #存在返回1
        else:
            db.close()
            return 0        #不存在返回0
    
    #计算表table_name中已用多少个数据，返回下一项数据对应的序号
    def amount(self,table_name):
        db = self._connect()
        cursor = db.cursor()
        sql="select * from "+ table_name
        result=cursor.execute(sql)
        db.commit()
        result=result+1
        print("server_index:\t",result)
        return result


    def _add_table_record( self, tablename,username):
        db = self._connect()
        cursor = db.cursor()
        sql = "INSERT INTO " + tablename + "(username,server_index) VALUE (%s, %s)"
        value=(username,self.amount(tablename))
        try:
            cursor.execute(sql, value)
            db.commit()
            print('数据插入成功！')
        except pymysql.Error as error:
            print("数据插入失败：" + str(error))
            db.rollback()
        finally:
            db.close()

    def add_table_record( self, tablename,username, pwd ):
        db = self.connect()
        cursor = db.cursor()
        sql = "INSERT INTO " + tablename + "(username,password) VALUE (%s, %s)"
        value=(username,pwd)
        try:
            cursor.execute(sql, value)
            db.commit()
            print('数据插入成功！')
        except pymysql.Error as error:
            print("数据插入失败：" + str(error))
            db.rollback()
        finally:
            db.close()
    
    def _create_table( self, tablename ):
        #连接本地数据库
        db = self._connect()
        #创建游标
        cur = db.cursor()

        try:
            #如果存在table_name表，则删除
            #cur.execute('DROP TABLE IF EXISTS ' + tablename )
            sqlQuery = '''CREATE TABLE ''' + tablename + '''(
                    username VARCHAR(100),
                    server_index INT(100)
            )'''
            cur.execute(sqlQuery)
            print("数据表创建完成！")
        except pymysql.Error as error:
            print("数据表创建失败：" + str(error))
            db.rollback()
        finally:
            db.close()

    def create_table( self, tablename ):
        #连接本地数据库
        db = self.connect()
        #创建游标
        cur = db.cursor()

        try:
            #如果存在table_name表，则删除
            cur.execute('DROP TABLE IF EXISTS ' + tablename )
            sqlQuery = '''CREATE TABLE ''' + tablename + '''(
                    username VARCHAR(100),
                    password VARCHAR(100)
            )'''
            cur.execute(sqlQuery)
            print("数据表创建完成！")
        except pymysql.Error as error:
            print("数据表创建失败：" + str(error))
            db.rollback()
        finally:
            db.close()


    def solve(self,u,p,b):#u username p pwd
        #u=hash((u,p))
        u=u+p
        m=hashlib.sha224()
        m.update(u.encode('utf-8'))
        m.digest()
        u=m.hexdigest()
        print('u:\t',u)
        h=int(u,16)
        print("H^b:\t",h)
        #TODO:将u进行盲化处理
        #H=h**b
        #取u前两个字节作为表名存储盲化后的用户名H
        #table_name=u.encode('utf-8')
        
        table_name=u[:4]
        #table_name=table_name.decode('utf-8', errors='ignore')
        table_name="bucket_"+table_name
        print(table_name)
        print("table_name:\t",table_name)
        #往表中插入数据：需判断表是否存在
        if self.table_exists(table_name) == 0:
            print(table_name+' not exists')
            self._create_table(table_name)
        self._add_table_record(table_name,u)


    def find(self):
        db = self.connect()
        cur = db.cursor()
        sqlQuery = "SELECT * FROM info"
        try:
            cur.execute(sqlQuery)
            results = cur.fetchall()
            b=10
            for data in results:
                username=data[0]
                pwd=data[1]
                print("username:"+username+" pwd:"+pwd)
                self.solve(username,pwd,b)
        except pymysql.Error as e:
            print("数据查询失败：" + str(e))
        finally:
            db.close()


def main():
    dbinfo = DataBaseInfo()
    # delete_database( self )
    # dbinfo.create_database(  )
    dbinfo.create_table( 'info' )
    for i in range(1000):
        user_name=i*100
        user_password=user_name
        dbinfo.add_table_record( 'info', user_name, user_password )
    dbinfo.find()

if __name__ == "__main__":
    main()