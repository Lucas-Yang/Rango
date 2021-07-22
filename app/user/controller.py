# /usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json

from fastapi import APIRouter
from app.common.data import UserLoginItem, UserRegisterItem
from app.common.factory import FormatCheck

user_app = APIRouter()
format_handler = FormatCheck()

@user_app.post('/register')
async def user_register(item: UserRegisterItem):
    """
    :return:
    """
    if format_handler.user_register_check(item):
        return item
    return


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









