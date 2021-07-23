""" 数据定义
"""

from pydantic import BaseModel
from typing import Optional
from app.common.data import ReturnCode

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