# /usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import time
import redis
import aioredis
from pymongo import MongoClient
from pymysql import IntegrityError

MONGO_URL = 'mongodb://burytest:GbnO35lpzAyjkPqSXQTiHwLuDs2r4gcR@172.22.34.102:3301/test' \
            '?authSource=burytest&replicaSet=bapi&readPreference=primary&appname=MongoDB%2' \
            '0Compass&ssl=false'
MONGO_DB = 'burytest'

MYSQL_HOST = "127.0.0.1"
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "test"
MYSQL_PORT = 3306


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
        self.db = pymysql.connect(host=self.host, port=self.port,
                                  user=self.username, password=self.password,
                                  db=self.database, charset='utf8'
                                  )
        self.cursor = self.db.cursor()

    def insert_db(self, sql: str):
        """数据插入
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except BaseException as error:
            print(error)
            self.db.rollback()
            raise Exception(error)
        finally:
            self.cursor.close()

    def delete_db(self, sql):
        """数据删除
        :param sql:
        :return:
        """
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
        try:
            # 执行sql
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as err:
            print(err)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def select_db(self, sql):
        """数据库查询
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            data = self.cursor.fetchall()  # 返回所有记录列表
            return data
        except Exception as err:
            print(err)
            print('Error: unable to fetch data')
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


class RedisClient(object):
    """ redis 操作封装类
    """
    def __init__(self, host='localhost', port=6379, decode_responses=True):
        """
        """
        self.__pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
        self.__redis_cli = redis.Redis(connection_pool=self.__pool)

    def insert_data(self, key=None, value=None):
        """
        """
        self.__redis_cli.set(key, value)

    def get_data(self, key):
        """
        """
        self.__redis_cli.get(key)

    def delete_data(self, key):
        """
        """

    def update_data(self, key):
        """
        """


if __name__ == "__main__":
    mysql_handler = MySQLClient()
    sql = "INSERT INTO t_user(email, password, role, status) VALUES ('1', '1', 1, 1)"
    mysql_handler.insert_db(sql)
    mysql_handler.close_db()
