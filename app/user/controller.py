# /usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.user.model import UserLoginItem, UserRegisterItem, UserUpdateItem, UserModelReturn
from app.common.factory import FormatCheck
from app.user.dao import UserDao
from app.user import oauth2_scheme
from app.common.db import RedisClient

user_app = APIRouter()
format_handler = FormatCheck()


@user_app.post('/register', response_model=UserModelReturn, summary="用户账号注册", tags=["用户模块"])
def user_register(item: UserRegisterItem):
    """
    :return:
    """
    if format_handler.user_register_check(item):
        user_handler = UserDao(item.dict())
        reg_status, msg = user_handler.user_register()
        if reg_status:
            return UserModelReturn(code=0, msg="success", data={"info": msg})
        else:
            return UserModelReturn(code=2, msg="internal error", data={"info": msg})
    else:
        return UserModelReturn(code=1, msg="input error")


@user_app.put('/update', response_model=UserModelReturn, summary="用户信息更新，主要是root管理员调用", tags=["用户模块"])
async def user_update(item: UserUpdateItem, token: str = Depends(oauth2_scheme)):
    """
    :return:
    """
    if format_handler.user_update_check(item):
        user_handler = UserDao(item.dict())
        reg_status, msg = user_handler.user_update(token=token)
        if reg_status:
            return UserModelReturn(code=0, msg="success", data={"info": msg})
        else:
            return UserModelReturn(code=2, msg="internal error", data={"info": msg})
    else:
        return UserModelReturn(code=1, msg="input error")


@user_app.get('/status', response_model=UserModelReturn, summary="用户身份查询", tags=["用户模块"])
async def user_status(token: str = Depends(oauth2_scheme)):
    """
    :return:
    """
    user_handler = UserDao()
    user_email = user_handler.user_auth(token)
    reg_status, msg = user_handler.admin_user_status(user_email)
    if reg_status:
        return UserModelReturn(code=0, msg="success", data={"data": msg})
    else:
        return UserModelReturn(code=2, msg="internal error", data={"info": msg})


@user_app.get('/admin-status', summary="管理员查询其他用户状态信息接口，不对外暴露", tags=["用户模块"])
async def admin_search_user_status(user_id, token: str = Depends(oauth2_scheme)):
    """
    :param user_id:
    :param token:
    :return:
    """
    if format_handler.user_status_check(user_id):

        user_handler = UserDao()
        ret_status, ret_info = user_handler.admin_search_user_status(token=token,
                                                                     search_user_email=user_id
                                                                     )
        if ret_status:
            return UserModelReturn(code=0, msg="success", data={"data": ret_info})
        else:
            return UserModelReturn(code=2, msg="internal error", data={"info": ret_info})
    else:
        return UserModelReturn(code=1,
                               msg="input error",
                               data={"info": "email is wrong, plz input right email"}
                               )


@user_app.post('/login', response_model=UserModelReturn, summary="用户登录（会自动调用获取token的api)", tags=["用户模块"])
async def user_login(item: UserLoginItem):
    """
    :return:
    """
    if format_handler.user_register_check(item):
        user_handler = UserDao(item.dict())
        acs_status, user_token = user_handler.user_login()
        if acs_status:
            return UserModelReturn(code=0, msg="success", data={"Token": user_token})
        else:
            return UserModelReturn(code=2, msg="internal error", data={"info": user_token})
    else:
        return UserModelReturn(code=1, msg="input error")


@user_app.post('/token', summary="swagger 获取token 非暴露给前端，前端通过login获取token", tags=["用户模块"])
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    :return:
    """
    user_handler = UserDao({"email": form_data.username, "password": form_data.password})
    acs_status, user_token = user_handler.user_login()
    return {
        "access_token": user_token,
        "token_type": 'Bearer'
    }


@user_app.get('/test-auth', summary="测试用户认证接口", tags=["用户模块"])
async def user_login(token: str = Depends(oauth2_scheme)):
    """
    :param token:
    :return:
    """
    user_handler = UserDao()
    return user_handler.user_auth(token)


@user_app.get('/verify/code', summary="获取验证玛", tags=["用户模块"])
async def get_verify_code(email):
    """
    :return
    """
    redis_handle = RedisClient()
    status, msg = redis_handle.async_create_verification_code(email)
    if status:
        return UserModelReturn(code=0, msg="success", data={"info": msg})
    else:
        return UserModelReturn(code=2, msg="internal error", data={"info": msg})


@user_app.get('/ping', summary="test", tags=["用户模块"])
async def test():
    """
    :return:
    """
    return {"code": 0, "msg": "hello Rango"}
