# 存放自定义的数据结构
from pydantic import BaseModel
from typing import Optional
from enum import Enum, unique


# ########################## 通用错误码定义 ###########################

@unique
class ReturnCode(Enum):
    """
    """
    SUCCESS = 0  # 成功
    INPUT_ERROR = 1  # 输入错误
    INTERNAL_ERROR = 2  # 内部错误
    SQL_ERROR = 3  # sql 错误
    UNKNOWN_ERROR = 4  # 未知错误


# ########################## bin 模块数据定义 ###########################
# 标注任务模块

# 评估任务模块

# ########################## user 模块数据定义 ###########################

class UserLoginItem(BaseModel):
    """ 用户模块-登陆数据
    """
    email: str
    password: str


class UserRegisterItem(BaseModel):
    """ 用户模块-注册
    """
    email: str
    password: str


class UserUpdateItem(BaseModel):
    """ 用户模块-用户信息更新
    """
    email: str
    role: str
    status: str


class UserModelReturn(BaseModel):
    """ 用户模块 - 返回值
    """
    code: ReturnCode
    msg: str
    data: Optional[dict]


if __name__ == '__main__':
    print(UserModelReturn)
