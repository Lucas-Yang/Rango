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
        user_handler = UserModel(item.json())
        return UserModelReturn(code=0, msg="success", data={"dd": 1})
    else:
        return UserModelReturn(code=1, msg="input error")


@user_app.put('/update')
async def user_login():
    """
    :return:
    """
    pass


@user_app.get('/status')
async def user_login(user_id: str):
    """
    :return:
    """
    pass


@user_app.post('/login')
async def user_login(item: UserLoginItem):
    """
    :return:
    """
    return item









