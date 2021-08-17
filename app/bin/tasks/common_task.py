""" 公共异步任务
异步任务队列， 主要处理耗时非紧急任务
"""
import itertools
import logging
import time
import uuid
from operator import itemgetter

from app.common.boss import Boss
from app.common import mongodb_client
from app.bin.tasks import celery_app as app


@app.task()
def upload_data(obj, task_id, group_id, video_index, file_name):
    db = mongodb_client
    collection = db['rango_task_files']
    fid = f'{uuid.uuid4()}'
    logging.info(fid)

    # insert mongo
    insert_data = {'task_id': task_id, 'group_id': group_id, 'video_index': video_index, 'fid': fid,
                   'file_name': file_name, 'status': 0}
    collection.insert_one(insert_data)
    del insert_data['_id']
    # upload
    boss = Boss()
    boss_url = boss.upload_data(obj, file_name)
    logging.info(boss_url)
    # update mongo
    select = {'fid': fid}
    update_set = {"$set": {'boss_url': boss_url, 'status': 1}}
    collection.update_many(select, update_set, upsert=True)
    return insert_data


@app.task()
def create_task(task_id, task_name, user, task_type, questionnaire_num, expire_date, task_detail={}):
    """
    created_at 创建日期
    updated_at 修改日期
    session_id 任务标识 唯一主键
    job_name 任务描述
    job_type  任务类型  标注,指标
    tasks  视频列表
    questionnaire_num 评估问卷数量
    collected_questionnaire_num  已收集的问卷数量
    expire_data 评估有效期
    """
    if task_detail != {}:
        task_detail["index_type"] = task_detail["index_type"].value
    else:
        pass
    db = mongodb_client
    file_col = db['rango_task_files']
    res = file_col.find({'task_id': task_id}, {'group_id': 1, 'video_index': 1, 'boss_url': 1, 'status': 1}).sort(
        [('group_id', 1)])
    # todo 根据 status判断是否现在执行
    groups = {}
    if res:
        for key, items in itertools.groupby(res, key=itemgetter('group_id')):
            groups[str(key)] = []
            [groups[str(key)].append(i['boss_url']) for i in sorted(items, key=lambda i: i['video_index'])]
    # todo 生成拼接视频
    collection = db['rango_evaluate_tasks']

    insert_data = {
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task_id": task_id,
        "task_name": task_name,
        "task_type": task_type,
        "groups": groups,
        "user": user,
        "questionnaire_num": questionnaire_num,
        "expire_data": expire_date,
        "task_detail": task_detail,
        "status": 0
    }
    collection.insert_one(insert_data)
