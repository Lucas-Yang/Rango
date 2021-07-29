# /usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json
import uuid
from fastapi import APIRouter
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.security import OAuth2PasswordBearer
from app.common.db import MyMongoClient
from app.bin.model import BinModelReturn, TaggingTaskCreate, TaggingTaskUpdate
import app.bin.task as task
import io
from app.bin.dao import TaggingDao

video_app = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/register')
db = MyMongoClient()

from app.bin.model import BinModelReturn, TaggingTaskCreate, TaggingTaskStatus, TaggingTaskScore
from app.user import oauth2_scheme

video_app = APIRouter()


@video_app.post('/tagging/task', response_model=BinModelReturn, summary="创建标注任务")
async def mos_video_task_create(item: TaggingTaskCreate):
    """ 创建标注任务接口
    :return:
    """
    task.create_tagging_task(item.task_id, item.job_name, item.user, item.job_type, item.questionnaire_num,
                             item.expire_data)
    return BinModelReturn(code=0, msg="success", data={"task_id": item.task_id})


@video_app.put('/tagging/task', response_model=BinModelReturn, summary="修改标注任务")
async def mos_video_task_update(item: TaggingTaskUpdate):
    """ 标注任务修改
    :return:
    """
    res = TaggingDao().modify_tagging_task(item)
    return BinModelReturn(code=0, msg="success", data={"modify_num": res})


@video_app.get('/get-task-id/')
async def get_task_task_id():
    session_id = f'{uuid.uuid4()}'
    """ 获取本次任务id
    :return:
    """
    return session_id[:12]


@video_app.get('/tagging/task/status', response_model=BinModelReturn, summary="标注任务查询")
async def mos_video_task_status(task_id: str):
    """ 标注任务查询
    :return:
    """

    res = TaggingDao().query_tagging_task(task_id=task_id)
    return BinModelReturn(code=0, msg="success", data={"task_info": res})


@video_app.get('/tagging/task-status', response_model=BinModelReturn, summary="用户标注任务查询")
async def mos_video_task_status_by_user(user: str, page_num: int, page_size: int):
    """ 标注任务查询
    :return:
    """

    res = TaggingDao().query_tagging_task_by_user(user=user, skip=page_num, limit_num=page_size)
    return BinModelReturn(code=0, msg="success", data={"task_info": res})



@video_app.delete('/tagging/task', response_model=BinModelReturn, summary="标注任务删除")
async def mos_video_task_delete(task_id: str):
    """ 标注任务删除

    """
    res = TaggingDao().delete_tagging_task(task_id=task_id)
    return BinModelReturn(code=0, msg="success", data={"task_delete_info": res})


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
def evaluate_video_task_delete(task_id: str, group_id: int, video_index: int, file: UploadFile = File(...)):
    """ 一个task粒度下，上传单个视频的接口
    :return:ss
    """
    file_content = io.BytesIO(file.file.read())
    insert_data = task.upload_data(file_content, task_id, group_id, video_index, file.filename)
    return BinModelReturn(code=0, msg="success", data={"file_name": file.filename, "file_address": str(insert_data)})


@video_app.delete('/task-file/delete', response_model=BinModelReturn, summary="单个文件删除")
async def evaluate_video_task_delete(fid: str):
    """ 一个task粒度下，删除单个视频的接口
    :return:
    """
    res = TaggingDao().delete_upload_file(fid=fid)
    return BinModelReturn(code=0, msg="success", data={"task_delete_info": res})
