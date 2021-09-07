# /usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread

import pymysql
import time
import redis
import uuid
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import aioredis
from pymongo import MongoClient
import config.config as config


class MySQLClient(object):
    """mysql 操作类
    """

    def __init__(self, host=config.mysql_config.get("host"),
                 username=config.mysql_config.get("username"),
                 password=config.mysql_config.get("password"),
                 database=config.mysql_config.get("database"),
                 port=config.mysql_config.get("port")):
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

    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MySQLClient, cls).__new__(cls)
        return cls.instance
    """

    def insert_db(self, sql: str):
        """数据插入
        :param sql:
        :return:
        """
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
        except BaseException as error:
            print(error)
            self.db.rollback()
            raise Exception(error)
        finally:
            cursor.close()

    def delete_db(self, sql):
        """数据删除
        :param sql:
        :return:
        """
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
        except BaseException as err:
            print(err)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            cursor.close()

    def update_db(self, sql):
        """数据刷新
        :param sql:
        :return:
        """
        cursor = self.db.cursor()
        try:
            # 执行sql
            cursor.execute(sql)
            self.db.commit()
        except Exception as err:
            print(err)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            cursor.close()

    def select_db(self, sql):
        """数据库查询
        :param sql:
        :return:
        """
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            data = cursor.fetchall()  # 返回所有记录列表
            return data
        except Exception as err:
            print(err)
            print('Error: unable to fetch data')
        finally:
            cursor.close()

    def close_db(self):
        """
        :return:
        """
        self.db.close()


class MyMongoClient(object):
    """mongo 操作类
    """

    def __init__(self):
        self.Mongo_client = MongoClient(config.mongo_config.get('mongodb_uri'), replicaSet="bapi", connect=False)
        self.db = self.Mongo_client.mobileautotest
        self.db.authenticate(name=config.mongo_config.get('mongodb_user'),
                             password=config.mongo_config.get('mongodb_password'))
        self.db_initial_time = time.strftime("%Y-%m-%d %H:%M:%S")

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
    def __init__(self,
                 host=config.redis_config.get('host'),
                 port=config.redis_config.get('port'),
                 decode_responses=True
                 ):
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
        value = self.__redis_cli.get(key)
        return value

    def delete_data(self, key):
        """
        """

    def update_data(self, key):
        """
        """

    def create_verification_code(self, email):
        temp = uuid.uuid4()
        v_code = str(temp).replace('-', '')[:6]

        # 存储数据库
        self.__redis_cli.set(email, v_code, ex=120)

        # 发送邮件
        sender = config.email_config.get('sender')
        password = config.email_config.get('password')

        # 发信服务器
        smtp_server = config.email_config.get('smtp_server')
        receiver = email
        body = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html";charset="utf-8">
        <title>verification code email</title>
        </head>
        <body>
        <p>本次注册的验证码:</p>
        <p><h1>{}</h1></p>
        </body>
        </html>
        """
        message = MIMEText(body.format(v_code), 'html', 'utf-8')
        message['From'] = Header(sender)
        message['To'] = Header(receiver)
        message['Subject'] = Header('rango 注册验证码', 'utf-8')

        try:
            server = smtplib.SMTP_SSL(smtp_server)
            server.connect(smtp_server, 465)
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
            server.close()
            return True, "验证码发送成功"
        except smtplib.SMTPException:
            raise Exception("邮件发送失败")

    def async_create_verification_code(self, email):
        """
        :param email:
        :return:
        """
        try:
            thread = Thread(target=self.create_verification_code, args=(email,))
            thread.start()
            return True, "验证码发送成功"
        except Exception as error:
            return False, str(error)


if __name__ == "__main__":
    redis_client = RedisClient()
    t1 = time.time()
    redis_client.create_verification_code("luoyadong@bilibili.com")
    print(time.time() - t1)
    print(redis_client.async_create_verification_code("luoyadong@bilibili.com"))
    print(time.time() - t1)
