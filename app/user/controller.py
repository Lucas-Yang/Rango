# /usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json

from fastapi import APIRouter

from app.common.data import UserLoginItem, UserRegisterItem, UserModelReturn
from app.common.factory import FormatCheck
from app.user.model import UserModel


user_app = APIRouter()
format_handler = FormatCheck()


@user_app.post('/register', response_model=UserModelReturn)
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


@user_app.put('/update')
async def user_login():
    """
    :return:
    """
    pass


@user_app.get('/status')
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


@user_app.post('/login', response_model=UserModelReturn)
async def user_login(item: UserLoginItem):
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









