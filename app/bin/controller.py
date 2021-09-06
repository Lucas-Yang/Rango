# /usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import io

from pymongo.errors import DuplicateKeyError

import app.bin.tasks.common_task as task
from fastapi import APIRouter, UploadFile, File, Depends, Cookie
from typing import Optional

from app.bin.model import BinModelReturn, TaggingTaskCreate, TaggingTaskStatus, \
    TaggingTaskScore, TaggingTaskUpdate, EvaluationTaskCreate, UserTaskStatus

from app.bin.dao import TaggingDao, EvaluationDao
from app.bin.tasks.evaluation_task import evaluation_task
from app.user import oauth2_scheme
from app.user.dao import UserDao

video_app = APIRouter()


# ################# 标注任务接口 ##################


@video_app.post('/tagging/task', response_model=BinModelReturn, summary="创建标注任务", tags=["tagging 模块"])
async def mos_video_task_create(item: TaggingTaskCreate):
    """ 创建标注任务接口
    :return:
    """
    task.create_task(item.task_id, item.task_name, item.user, item.task_type, item.questionnaire_num,
                     item.expire_data)
    return BinModelReturn(code=0, msg="success", data={"task_id": item.task_id})


@video_app.put('/tagging/task', response_model=BinModelReturn, summary="修改标注任务", tags=["tagging 模块"])
async def mos_video_task_update(item: TaggingTaskUpdate):
    """ 标注任务修改
    :return:
    """
    res = TaggingDao().modify_tagging_task(item)
    return BinModelReturn(code=0, msg="success", data={"modify_num": res})


@video_app.get('/tagging/task-status', response_model=BinModelReturn, summary="用户标注任务查询", tags=["tagging 模块"])
async def mos_video_task_status_by_user(user: str, page_num: int = 1, page_size: int = 10):
    """ 标注任务查询
    :return:
    """

    res, count = TaggingDao().query_tagging_task_by_user(user=user, skip=page_num, limit_num=page_size)
    return BinModelReturn(code=0, msg="success", data={"task_info": res, "count": count})


@video_app.get('/tagging/task-group-info', response_model=BinModelReturn, summary="查询task对应group的url", tags=["tagging 模块"])
async def mos_video_task_task_group_info(task_id: str, group_id: int = 1):
    """ 标注任务查询
    :return:
    """

    res = TaggingDao().query_tagging_task_by_index(task_id=task_id, index=group_id)
    return BinModelReturn(code=0, msg="success", data={"groups_info": res})


@video_app.delete('/tagging/task', response_model=BinModelReturn, summary="标注任务删除", tags=["tagging 模块"])
async def mos_video_task_delete(task_id: str):
    """ 标注任务删除

    """
    res = TaggingDao().delete_tagging_task(task_id=task_id)
    return BinModelReturn(code=0, msg="success", data={"task_delete_info": res})


@video_app.post('/tagging/group/score', response_model=BinModelReturn, summary="评估任务打分回收", tags=["tagging 模块"])
async def moss_video_task_score(item: TaggingTaskScore):
    """
    插入标注视频分数
    :return:
    """
    res = TaggingDao().collect_video_task_score(dict(item))

    print(res.inserted_id)
    return BinModelReturn(code=0, msg="success", data={"insert_info": dict(item)})


@video_app.post('/tagging/task/user', response_model=BinModelReturn, summary="记录用户完成的task", tags=["tagging 模块"])
async def moss_video_record_task_user(item: UserTaskStatus):
    """
    记录用户完成的task
    :return:
    """
    TaggingDao().record_tagging_task_user(dict(item))
    return BinModelReturn(code=0, msg="success", data={"insert_info": item.user})


@video_app.post('/tagging/task/score', response_model=BinModelReturn, summary="计算标注任务打分", tags=["tagging 模块"])
async def moss_video_computed_task_score(task_id: str):
    """
    插入标注视频分数
    :return:
    """
    res = TaggingDao().computed_video_task_scores(task_id)

    return BinModelReturn(code=0, msg="success", data={"insert_info": res})


@video_app.get('/tagging/task/score/user', response_model=BinModelReturn, summary="用户已标记的任务", tags=["tagging 模块"])
async def moss_video_query_user_task(user: str, page_num: int = 1, page_size: int = 10):
    """
    查询对应用户已标注的task
    :return:
    """
    res, count = TaggingDao().video_query_user_task(user, page_num, page_size)
    return BinModelReturn(code=0, msg="success", data={"data": res, "count": count})

@video_app.get('/tagging/task/score', response_model=BinModelReturn, summary="用户已标记的任务", tags=["tagging 模块"])
async def video_query_task_score(task_id: str):
    """
    查询对应用户已标注的task
    :return:
    """
    res = TaggingDao().video_query_task_score(task_id)
    return BinModelReturn(code=0, msg="success", data={"data": res})
# ############## 自动评估接口 ###############


@video_app.post('/evaluation/task', response_model=BinModelReturn, summary="评估任务创建", tags=["evaluation 模块"])
async def evaluate_video_task_create(item: EvaluationTaskCreate):
    """ 评估任务创建
    :return:
    """
    # user_handler = UserDao()
    # user_name = user_handler.user_auth(token)
    try:
        task.create_task(item.task_id, item.task_name, item.user,
                         item.task_type, item.questionnaire_num,
                         item.expire_data, task_detail=item.task_details.dict()
                         )
    except DuplicateKeyError as err:
        return BinModelReturn(code=3, msg="db error", data={"error_detail": str(err)})
    r = evaluation_task.delay(item.task_id)
    return BinModelReturn(code=0, msg="success", data={"async_task_id": r.task_id})


@video_app.put('/evaluation/task', response_model=BinModelReturn, summary="评估任务修改", tags=["evaluation 模块"])
async def evaluate_video_task_update(token: str = Depends(oauth2_scheme)):
    """ 评估任务修改
    :return:
    """
    pass


@video_app.delete('/evaluation/task', response_model=BinModelReturn, summary="评估任务删除", tags=["evaluation 模块"])
async def evaluate_video_task_delete(task_id: str, token: str = Depends(oauth2_scheme)):
    """ 评估任务删除
    :return:
    """
    user_handler = UserDao()
    user_name = user_handler.user_auth(token)
    evaluate_client = EvaluationDao()
    evaluate_client.delete_evaluation_task(user_id=user_name, task_id=task_id)
    return BinModelReturn(code=0, msg="success", data={"task_id": task_id})


@video_app.get('/evaluation/task', response_model=BinModelReturn, summary="用户个人创建评估任务查询", tags=["evaluation 模块"])
async def personal_evaluate_video_task_status(user: str):
    """
    :param:

    user：用户名 前端从cookie中获取

    :return example:
    直接查询： luoyadong@bilibili.com 查看具体的返回格式
    """
    # user_handler = UserDao()
    # user_name = user_handler.user_auth(token)
    evaluate_client = EvaluationDao()
    personal_task_info = evaluate_client.get_task_personal_result(user)
    return BinModelReturn(code=0, msg="success", data={"result_list": personal_task_info})


# ################# 文件上传 ##################


@video_app.post('/task-file/upload', response_model=BinModelReturn, summary="单个文件上传到boss接口", tags=["bin辅助模块"])
def evaluate_video_task_delete(task_id: str, group_id: int, video_index: int, file: UploadFile = File(...)):
    """ 一个task粒度下，上传单个视频的接口
    :return:ss
    """
    # user_handler = UserDao()
    # user_name = user_handler.user_auth(token)
    file_content = io.BytesIO(file.file.read())
    insert_data = task.upload_data(file_content, task_id, group_id, video_index, file.filename)
    return BinModelReturn(code=0, msg="success", data={"file_name": file.filename, "file_address": str(insert_data)})


@video_app.delete('/task-file/delete', response_model=BinModelReturn, summary="单个文件删除", tags=["bin辅助模块"])
async def evaluate_video_task_delete(fid: str):
    """ 一个task粒度下，删除单个视频的接口
    :return:
    """
    # user_handler = UserDao()
    # user_name = user_handler.user_auth(token)
    res = TaggingDao().delete_upload_file(fid=fid)
    return BinModelReturn(code=0, msg="success", data={"task_delete_info": res})


@video_app.get('/task-file/groups', response_model=BinModelReturn, summary="查询group的filelist", tags=["bin辅助模块"])
async def evaluate_video_task_query(task_id: str):
    """ 查询单个task_id 下的group 和video 详情
    :return:
    """
    # user_handler = UserDao()
    # user_name = user_handler.user_auth(token)
    res = TaggingDao().query_upload_file_by_task_id(task_id=task_id)
    return BinModelReturn(code=0, msg="success", data={"task_groups_info": res})


@video_app.get('/get-task-id', response_model=BinModelReturn, summary="生成任务id", tags=["bin辅助模块"])
async def get_task_task_id():
    """ 获取本次任务id
    :return:
    """
    # user_handler = UserDao()
    # user_name = user_handler.user_auth(token)
    session_id = f'{uuid.uuid4()}'
    return BinModelReturn(code=0, msg="success", data={"task_id": session_id[:12]})

