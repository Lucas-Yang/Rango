""" 数据交互
"""
from app.common.db import MySQLClient


class UserModel(object):
    """
    """
    def __init__(self, item: dict):
        """
        """
        self.item = item
        self.__mysql_handler = MySQLClient()

    def user_register(self):
        """
        :return:
        """
        mysql_handler = MySQLClient()
        sql = "INSERT INTO t_user(email, password, role, status) VALUES ({}, {}, 1, 1)".\
            format(self.item.get("email"), self.item.get("password"))
        mysql_handler.insert_db(sql)

    def user_login(self):
        """
        :return:
        """

    def user_status(self):
        """
        :return:
        """

    def close_model(self):
        self.__mysql_handler.close_db()