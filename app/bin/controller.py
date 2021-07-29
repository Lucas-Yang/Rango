# /usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json
import uuid
from fastapi import APIRouter
from fastapi import APIRouter, UploadFile, File, Depends

from app.bin.model import BinModelReturn, TaggingTaskCreate, TaggingTaskStatus, TaggingTaskScore
from app.user import oauth2_scheme

video_app = APIRouter()


@video_app.post('/tagging/task', response_model=BinModelReturn, summary="创建标注任务")
async def mos_video_task_create(item: TaggingTaskCreate, token: str = Depends(oauth2_scheme)):
    """ 标注任务接口
    :return:
    """
    pass


@video_app.put('/tagging/task')
async def mos_video_task_update():
    """ 标注任务修改
    :return:
    """
    pass



@video_app.get('/get_task_sessionid/')
async def get_task_sessionid():
    session_id =  uuid.uuid4()
    """ 获取本次任务id
    :return:
    """
    return session_id[:14]


@video_app.get('/tagging/task/status', response_model=BinModelReturn, summary="标注任务查询")
async def mos_video_task_status(task_id: str):
    """ 标注任务查询
    :return:
    """
    pass


@video_app.get('/tagging/task/single-status', response_model=BinModelReturn, summary="单条评估任务查询")
async def single_evaluate_video_task_status(task_id: str):
    """
    :return:
    """
    pass


@video_app.get('/tagging/task/personal-status', response_model=BinModelReturn, summary="用户个人创建评估任务查询")
async def personal_evaluate_video_task_status(user_id: str):
    """
    :return:
    """
    pass


@video_app.post('/tagging/task/score', response_model=BinModelReturn, summary="评估任务打分回收")
async def moss_video_task_score(item: TaggingTaskScore):
    """
    :return:
    """
    print(item)


# ############## 自动评估接口 ###############


@video_app.post('/evaluation/task', response_model=BinModelReturn, summary="评估任务创建")
async def evaluate_video_task_create():
    """ 评估任务创建
    :return:
    """
    pass


@video_app.put('/evaluation/task', response_model=BinModelReturn, summary="评估任务修改")
async def evaluate_video_task_update():
    """ 评估任务修改
    :return:
    """
    pass


@video_app.get('/evaluation/task/single-status', response_model=BinModelReturn, summary="单条评估任务查询")
async def single_evaluate_video_task_status(task_id: str):
    """
    :return:
    """
    pass


@video_app.get('/evaluation/task/personal-status', response_model=BinModelReturn, summary="用户个人创建评估任务查询")
async def personal_evaluate_video_task_status(user_id: str):
    """
    :return:
    """
    pass


@video_app.get('/evaluation/task/status', response_model=BinModelReturn, summary="评估任务总查询")
async def evaluate_video_task_status(item: TaggingTaskStatus):
    """
    :return:
    """
    pass


@video_app.delete('/evaluation/task', response_model=BinModelReturn, summary="评估任务删除")
async def evaluate_video_task_delete():
    """ 评估任务删除
    :return:
    """
    pass


@video_app.post('/task-file/upload', response_model=BinModelReturn, summary="单个文件上传到boss接口")
async def evaluate_video_task_delete(file: UploadFile = File(...)):
    """ 一个task粒度下，上传单个视频的接口
    :return:
    """
    file_content = await file.read()
    file_boss_url = ""
    return BinModelReturn(code=0, msg="success", data={"file_name": file.filename(), "file_address": file_boss_url})


@video_app.delete('/task-file/delete', response_model=BinModelReturn, summary="单个文件删除")
async def evaluate_video_task_delete():
    """ 一个task粒度下，删除单个视频的接口
    :return:
    """
    pass
