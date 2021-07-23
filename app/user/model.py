""" 数据交互
"""

from app.common.db import MySQLClient


class UserModel(object):
    """
    """
    def __init__(self, item: dict = None):
        """
        """
        self.item = item
        self.__mysql_handler = MySQLClient()

    def user_register(self):
        """
        :return:
        """
        try:
            sql = "INSERT INTO t_user(email, password, role, status) VALUES ({}, {}, 'common', 1)". \
                format('\'' + self.item.get("email") + '\'', self.item.get("password"))
            self.__mysql_handler.insert_db(sql)
            return True, "register success!"
        except Exception as error:
            return False, str(error)

    def user_update(self):
        """ 用户信息更新
        :return:
        """
        try:
            sql = "UPDATE t_user SET role='{}',status='{}'  WHERE email = '{}'". \
                format(self.item.get("role"),
                       self.item.get("status"),
                       self.item.get("email")
                       )
            self.__mysql_handler.insert_db(sql)
            return True, "update success!"
        except Exception as error:
            return False, str(error)

    def user_login(self):
        """
        :return:
        """
        pass

    def user_status(self):
        """
        :return:
        """
        try:
            sql = "select email, role, status from t_user where email = '{}'". \
                format(self.item.get("email"))
            data = self.__mysql_handler.select_db(sql)
            if data:
                return True, {"email": data[0][0], "role": data[0][1], "status": data[0][1]}
            else:
                return True, {}
        except Exception as error:
            return False, str(error)

    def close_model(self):
        self.__mysql_handler.close_db()
