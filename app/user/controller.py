# /usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json

from fastapi import APIRouter
from app.common.data import UserLoginItem

user_app = APIRouter()


@user_app.post('/register')
async def user_register():
    """
    :return:
    """
    pass


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









