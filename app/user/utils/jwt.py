import jwt
from datetime import datetime, timedelta
from typing import Optional


class UserJwt(object):
    """
    """
    def __init__(self, user_info_item: dict = None):
        """
        """
        self.__user_info_item = user_info_item
        self.__SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
        self.__ALGORITHM = "HS256"

    def create_access_token(self,  expires_delta: Optional[timedelta] = None):
        to_encode = self.__user_info_item
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=1500)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)
        return encoded_jwt

    def check_jwt_token(self, token: Optional[str] = None):
        """
        :param token:
        :return:
        """

        try:
            payload = jwt.decode(
                token,
                self.__SECRET_KEY, algorithms=[self.__ALGORITHM]
            )
            return payload
        except (jwt.ExpiredSignatureError, AttributeError):
            # 抛出自定义异常， 然后捕获统一响应
            raise Exception("access token fail")
