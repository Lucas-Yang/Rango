""" 数据交互
"""
from fastapi import HTTPException, status

from app.common.db import MySQLClient
from app.user.utils.jwt import UserJwt


class UserDao(object):
    """
    """
    def __init__(self, item: dict = None):
        """
        """
        self.item = item
        self.__mysql_handler = MySQLClient()
        self.__jwt_handler = UserJwt(self.item)

    def user_register(self):
        """
        :return:
        """
        try:
            sql = "INSERT INTO user(u_email, u_password, role, status) VALUES ({}, {}, 'common', 1)". \
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
            sql = "UPDATE user SET role='{}',status='{}'  WHERE u_email = '{}'". \
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
        try:
            user_status, user_info = self.user_status()
            if user_status:
                acs_token = self.__jwt_handler.create_access_token()
                return True, acs_token
            else:
                return False, user_info
        except Exception as err:
            return False, str(err)

    def user_status(self):
        """
        :return:
        """
        try:
            sql = "select u_email, role, status, u_password from user where u_email = '{}'". \
                format(self.item.get("email"))
            data = self.__mysql_handler.select_db(sql)
            print(data)
            if data:
                if data[0][3] == self.item.get("password"):
                    return True, {"email": data[0][0], "role": data[0][1], "status": data[0][2]}
                else:
                    return False, "密码错误"
            else:
                return False, "用户未注册"
        except Exception as error:
            return False, str(error)

    def user_auth(self, token):
        """ 用户认证
        :return:
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证失败",
            headers={'WWW-Authenticate': "Bearer"}
        )
        # 验证token
        try:
            payload = self.__jwt_handler.check_jwt_token(token)
            user_email = payload.get('email')
            if not user_email:
                raise credentials_exception
            else:
                return user_email
        except Exception as e:
            print(f'认证异常: {e}')
            raise credentials_exception

    def close_model(self):
        self.__mysql_handler.close_db()
