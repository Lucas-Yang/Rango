""" 数据交互
"""
from fastapi import HTTPException, status
from functools import singledispatch

from app.common.db import MySQLClient, RedisClient
from app.user.utils.jwt import UserJwt

# 用于加密数据
import hashlib


class UserDao(object):
    """
    """

    def __init__(self, item: dict = None):
        """
        """
        self.item = item
        self.__mysql_handler = MySQLClient()
        self.__jwt_handler = UserJwt(self.item)
        self.__redis_handle = RedisClient()

    def user_register(self):
        """
        :return:
        """
        try:
            user_status, user_info = self.user_status()
            # 密码sha256加密
            password_sha = hashlib.sha256(self.item.get("password").encode('utf-8')).hexdigest()

            v_code = self.__redis_handle.get_data(self.item.get("email", ""))
            if v_code is None or self.item.get("vcode") != v_code:
                return False, "verification code wrong or expired"
            if not user_status:
                if self.item.get("email", "").endswith("bilibili.com"):
                    user_role = "'master'"
                else:
                    user_role = "'common'"
                sql = "INSERT INTO user(u_email, u_password, role, status) VALUES ({}, {}, {}, 1)". \
                    format('\'' + self.item.get("email") + '\'', '\'' +
                           password_sha + '\'',
                           user_role
                           )
                self.__mysql_handler.insert_db(sql)
                return True, "register success!"
            else:
                return False, "register failed, user exist"
        except Exception as error:
            return False, str(error)

    def user_update(self, token):
        """ 用户信息更新, 只有管理员有权限
        :return:
        """
        try:
            update_email = self.user_auth(token)
            update_user_status, update_user_info = self.admin_user_status(update_email)
            if update_user_info.get("role", "") == "root":
                user_status, user_info = self.admin_user_status(self.item.get("email"))
                if user_status:
                    sql = "UPDATE user SET role='{}',status='{}'  WHERE u_email = '{}'". \
                        format(self.item.get("role"),
                               self.item.get("status"),
                               self.item.get("email")
                               )
                    self.__mysql_handler.insert_db(sql)
                    return True, "update success!"
                else:
                    return False, "update failed, {}".format(user_info)
            else:
                return False, "u have no right to update user info, because u are not admin user"
        except Exception as error:
            return False, str(error)

    def user_login(self):
        """ 注册时候密码未加密，后续完善
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
            if data:
                password_sha = hashlib.sha256(self.item.get("password").encode('utf-8')).hexdigest()
                if data[0][3] == password_sha:
                    return True, {"email": data[0][0], "role": data[0][1], "status": data[0][2]}
                else:
                    return False, "密码错误"
            else:
                return False, "用户未注册"
        except Exception as error:
            return False, str(error)

    # @overload @user_status.register(str)
    def admin_user_status(self, email):
        """ root用户的查询
        :param email:
        :return:
        """
        try:
            sql = "select u_email, role, status, u_password from user where u_email = '{}'". \
                format(email)
            data = self.__mysql_handler.select_db(sql)
            if data:
                return True, {"email": data[0][0], "role": data[0][1], "status": data[0][2]}
            else:
                return False, "用户未注册"
        except Exception as error:
            return False, str(error)

    def admin_search_user_status(self, token, search_user_email):
        """ 管理员查询其他用户的接口
        :param token:
        :param search_user_email:
        :return:
        """
        admin_user_email = self.user_auth(token)
        search_status, user_info = self.admin_user_status(admin_user_email)
        if search_status:
            user_role = user_info.get("role")
            if user_role == 'root':
                return self.admin_user_status(search_user_email)
            else:
                return False, "u have not right to query user info"
        else:
            return False, user_info

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


if __name__ == '__main__':
    handler = UserDao()
    print(handler.admin_user_status("luoyadong@bilibili.com"))
