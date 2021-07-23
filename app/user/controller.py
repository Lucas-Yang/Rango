# /usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json

from fastapi import APIRouter

from app.common.data import UserLoginItem, UserRegisterItem, UserUpdateItem, UserModelReturn
from app.common.factory import FormatCheck
from app.user.model import UserModel


user_app = APIRouter()
format_handler = FormatCheck()


@user_app.post('/register', response_model=UserModelReturn, summary="用户账号注册")
def user_register(item: UserRegisterItem):
    """
    :return:
    """
    if format_handler.user_register_check(item):
        user_handler = UserModel(item.dict())
        reg_status, msg = user_handler.user_register()
        if reg_status:
            return UserModelReturn(code=0, msg="success", data={"info": msg})
        else:
            return UserModelReturn(code=2, msg="internal error", data={"info": msg})
    else:
        return UserModelReturn(code=1, msg="input error")


@user_app.put('/update', response_model=UserModelReturn, summary="用户信息更新，主要是root管理员调用")
async def user_update(item: UserUpdateItem):
    """
    :return:
    """
    if format_handler.user_update_check(item):
        user_handler = UserModel(item.dict())
        reg_status, msg = user_handler.user_update()
        if reg_status:
            return UserModelReturn(code=0, msg="success", data={"info": msg})
        else:
            return UserModelReturn(code=2, msg="internal error", data={"info": msg})
    else:
        return UserModelReturn(code=1, msg="input error")


@user_app.get('/status', response_model=UserModelReturn, summary="用户身份查询")
async def user_status(user_id: str):
    """
    :return:
    """
    if format_handler.user_status_check(user_id):
        user_handler = UserModel({"email": user_id})
        reg_status, msg = user_handler.user_status()
        if reg_status:
            return UserModelReturn(code=0, msg="success", data={"data": msg})
        else:
            return UserModelReturn(code=2, msg="internal error", data={"info": msg})
    else:
        return UserModelReturn(code=1, msg="input error")


@user_app.post('/login', response_model=UserModelReturn, summary="用户登录（会自动调用获取token的api)")
async def user_login(item: UserLoginItem):
    """
    :return:
    """
    if format_handler.user_register_check(item):
        user_handler = UserModel(item.dict())
        reg_status, msg = user_handler.user_login()
        if reg_status:
            return UserModelReturn(code=0, msg="success", data={"info": msg})
        else:
            return UserModelReturn(code=2, msg="internal error", data={"info": msg})
    else:
        return UserModelReturn(code=1, msg="input error")

