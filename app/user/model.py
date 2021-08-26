""" 数据定义
"""
from enum import unique, Enum

from pydantic import BaseModel
from typing import Optional
from app.common.data import ReturnCode

# ########################## user 模块数据定义 ###########################


@unique
class UserRoleType(Enum):
    """
    """
    ROOT = 0  # 最高权限
    MASTER = 1  # 可以创建任务
    COMMON = 2  # 最普通权限，只能做标注任务


class UserLoginItem(BaseModel):
    """ 用户模块-登陆数据

    email 用户邮箱，作为用户id 唯一

    password 用户密码
    """
    email: str
    password: str


class UserRegisterItem(BaseModel):
    """ 用户模块-注册

    email 用户邮箱，作为用户id 唯一

    password 用户密码

    vcode 验证码

    """
    email: str
    password: str
    # vcode: str


class UserUpdateItem(BaseModel):
    """ 用户模块-用户信息更新

    email 用户id

    role 用户角色(common master root, 注册都是common，只有root用户可以修改其他人的角色)

    status 是否封禁该用户
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


# ########################## user jwt ###########################


class TokenItem(BaseModel):
    """ jwt token
    """
    access_token: str
    token_type: str
