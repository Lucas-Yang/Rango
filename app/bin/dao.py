# from app.bin.model import TaggingTaskUpate
import app.bin.model as model
import app.bin.dao as sql
from app.common.db import MyMongoClient
import time

""" 为接口生产数据
"""
db = MyMongoClient().db


class TaggingDao():
    """
    """

    def __init__(self):
        pass

    def query_tagging_task(self, task_id):
        task_col = db['rango_evaluate_tasks']
        res = task_col.find_one({'task_id': task_id}, {'_id': 0})
        return res

    def query_tagging_task_by_user(self, user, skip, limit_num):
        task_col = db['rango_evaluate_tasks']
        if user == 'all':
            user = {'$regex': '.*'}
        skip = (skip - 1) * limit_num
        res = list(task_col.find({'user': user}, {'_id': 0}).skip(skip).limit(limit_num))
        return res

    def delete_tagging_task(self, task_id):
        task_col = db['rango_evaluate_tasks']
        res = task_col.delete_one({'task_id': task_id})
        return res.deleted_count

    def modify_tagging_task(self, query: model.TaggingTaskUpdate):
        task_col = db['rango_evaluate_tasks']
        query = {'task_id': query.task_id}
        update = {"$set": {'updated_at': time.strftime("%Y-%m-%d %H:%M:%S")}}

        if query.result:
            update['job_name'] = query.job_name

        if query.similarity:
            update['questionnaire_num'] = query.questionnaire_num

        if query.casename:
            update['expire_data'] = query.expire_data

        if query.status:
            update['status'] = query.status
        res = task_col.update_one(query, update)
        return res

    def delete_upload_file(self, fid):
        file_col = db['rango_task_files']
        res = file_col.delete_one({'fid': fid})
        return res.deleted_count


class EvluationDao():
    """
    """
