# /usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import time
from pymongo import MongoClient

MONGO_URL = 'mongodb://burytest:GbnO35lpzAyjkPqSXQTiHwLuDs2r4gcR@172.22.34.102:3301/test' \
            '?authSource=burytest&replicaSet=bapi&readPreference=primary&appname=MongoDB%2' \
            '0Compass&ssl=false'
MONGO_DB = 'burytest'

MYSQL_HOST = "ops-db-5129-w-3308.testdb.bilibili.co"
MYSQL_USERNAME = "hassan"
MYSQL_PASSWORD = "4OLl5gQzFfvMUjT2PeswaBGuEi7YJRm3"
MYSQL_DATABASE = "hassan"
MYSQL_PORT = 3308


class MySQLClient(object):
    """mysql 操作类
    """

    def __init__(self, host=MYSQL_HOST, username=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                 database=MYSQL_DATABASE, port=MYSQL_PORT):
        """init
        :param host:
        :param username:
        :param password:
        :param database:
        :param port:
        """
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, self.port, charset='utf8')

    def insert_db(self, sql):
        """数据插入
        :param sql:
        :return:
        """
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except BaseException as error:
            print(error)
            self.db.rollback()
            raise Exception("db insert error")
        finally:
            self.cursor.close()

    def delete_db(self, sql):
        """数据删除
        :param sql:
        :return:
        """
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except BaseException as err:
            print(err)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def update_db(self, sql):
        """数据刷新
        :param sql:
        :return:
        """
        self.cursor = self.db.cursor()
        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def select_db(self, sql):
        """数据库查询
        :param sql:
        :return:
        """
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            data = self.cursor.fetchall()  # 返回所有记录列表
            return data
        except:
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()

    def close_db(self):
        """
        :return:
        """
        self.db.close()


class MyMongoClient(object):
    """mongo 操作类
    """

    def __init__(self):
        client = MongoClient(MONGO_URL, connect=False)
        self.db = client.get_database(MONGO_DB)
        self.db_initial_time = time.strftime("%Y-%m-%d %H:%M:%S")

    def db(self):
        """
        :return:
        """
        return self.db

    def insert(self, collection, data):
        """
        :param collection:
        :param data:
        :return:
        """
        if not isinstance(data, dict):
            raise Exception("args `data` is not dict, plz check!")
        data['create_time'] = self.db_initial_time
        self.db.get_collection(collection).insert_one(data)

    def query(self, collection, select=None):
        """
        :param collection:
        :param select:
        :return:
        """
        return self.db.get_collection(collection).find(select, no_cursor_timeout=True)


if __name__ == "__main__":
    mongo_client = MyMongoClient()
    # mongo_client.insert('fuzz_data', {"ip": "127.0.0.1", "age": 0, "path": "x1/name"})
    cursor = mongo_client.query('fuzz_data', {"path": "/x/resource/fission/check/device"}).sort("create_time",
                                                                                                -1).limit(1)
    for data in cursor:
        print(data)
