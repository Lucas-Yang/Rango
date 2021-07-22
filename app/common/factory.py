import re

from jsonschema import validate

from app.common.logger import LogManager


class FormatCheck(object):
    """
    输入格式检查
    """

    def __init__(self):
        self.__loger = LogManager().logger

    def user_register_check(self, register_item):
        """ 用户管理 - 注册校验
        :param register_item:
        :return:
        """
        email_pattern = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
        password_pattern = "(.*)"
        try:
            if re.match(email_pattern, register_item.email, re.M | re.I):
                return True
            else:
                return False
        except BaseException as err:
            self.__loger.error(err)
            return False

    def user_status_check(self, user_email):
        """
        :param user_email:
        :return:
        """
        email_pattern = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
        try:
            if re.match(email_pattern, user_email, re.M | re.I):
                return True
            else:
                return False
        except BaseException as err:
            self.__loger.error(err)
            return False


if __name__ == '__main__':
    handler = FormatCheck()
    print(handler.user_register_check(11))
