# 存放自定义的数据结构
from pydantic import BaseModel
from enum import Enum

# ########################## 通用错误码定义 ###########################


class ErrorCode(Enum):
    """
    """
    SUCCESS = {"0": "成功"}
    FAIL = {"1": "输入参数错误"}
    PARAM_IS_NULL = {"2": "内部错误"}
    SQL_ERROR = {"3": "数据库异常"}
    UNKNOWN_ERROR = {"4": "未知异常"}


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


class UserModelReturn(BaseModel):
    """ 用户模块 - 返回值
    """
    code: int
    msg: str
    data: dict
