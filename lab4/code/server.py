from flask import Flask, jsonify, request
import re
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship, backref
from flask_cors import *
import pymysql
import json

def _connect():
    '''连接MySQL数据库'''
    try:
        db = pymysql.connect(
            host='localhost',
            port=3306,
            user='gpc',
            passwd='gpc',
            db='c3server_v3',
            charset='utf8'
            )
        return db
    except Exception:
        raise Exception("数据库连接失败")

server=Flask(__name__)
CORS(server, supports_credentials=True)
server.config['DEBUG'] = False

def table_exists(table_name):        #这个函数用来判断表是否存在
    db = _connect()
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

@server.route('/api/requests', methods=['POST'])
def requests():
    start = datetime.datetime.now()
    get_data = json.loads(request.get_data(as_text=True))
    tablename=get_data['table_name']
    H=get_data['H']
    print(H)

    if table_exists(tablename) == 0:
        print(tablename+' not exists')
        end = datetime.datetime.now()
        print("using time:\t",end-start)
        return jsonify(result="none")
    else:
        db = _connect()
        cur = db.cursor()
        sqlQuery = "SELECT * FROM "+tablename
        try:
            cur.execute(sqlQuery)
            results = cur.fetchall()
            for data in results:
                if int(H) == int(data[0]):
                    db.close()
                    end = datetime.datetime.now()
                    print("using time:\t",end-start)
                    return jsonify(result="match")
            end = datetime.datetime.now()
            print("using time:\t",end-start)
            return jsonify(result="none") 
        except pymysql.Error as e:
            print("数据查询失败：" + str(e))
    
if __name__ == '__main__':
    server.run()