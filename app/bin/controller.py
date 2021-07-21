# /usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json

from fastapi import APIRouter

video_app = APIRouter()


@video_app.post('/tagging/task')
async def mos_video_task_create():
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


@video_app.get('/tagging/task/status')
async def mos_video_task_status(task_id: str):
    """ 标注任务查询
    :return:
    """
    pass


@video_app.delete('/tagging/task')
async def mos_video_task_delete():
    """ 标注任务删除
    :return:
    """
    pass


@video_app.post('/evaluation/task')
async def evaluate_video_task_create():
    """ 评估任务创建
    :return:
    """
    pass


@video_app.put('/evaluation/task')
async def evaluate_video_task_update():
    """ 评估任务修改
    :return:
    """
    pass


@video_app.get('/evaluation/task/status')
async def evaluate_video_task_status(task_id: str):
    """ 评估任务查询
    :return:
    """
    pass


@video_app.delete('/evaluation/task')
async def evaluate_video_task_delete():
    """ 评估任务删除
    :return:
    """
    pass
