# from app.bin.model import TaggingTaskUpate
import app.bin.model as model
import app.bin.dao as sql
from app.common.db import MyMongoClient
import time

# from app.bin.utils.Evaluation import FRVideoEvaluationFactory
# from app.bin.utils.Evaluation import NRVideoEvaluationFactory
""" 为接口生产数据
"""
db = MyMongoClient().db


class TaggingDao():
    """

    数据标准层数据接口
    """

    def __init__(self):
        pass

    def query_tagging_task(self, task_id):
        task_col = db['rango_evaluate_tasks']
        res = task_col.find_one({'task_id': task_id}, {'_id': 0})
        return res

    def query_tagging_task_by_user(self, user, skip, limit_num):
        """ 获取所有的待标注任务
        todo  添加status
        :param:
        :return:
        """
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

    def collect_video_task_score(self, score_info: dict):
        score_col = db['rango_tagging_score']
        res = score_col.insert_one(score_info)
        return res

    def video_query_task_score(self, task_id: str):
        score_col = db['rango_tagging_score_summary']
        res = score_col.find_one({'task_id': task_id}, {'scores': 1, '_id': 0})
        return res

    def computed_video_task_scores(self, task_id):
        score_col = db['rango_tagging_score']
        task_infos = list(score_col.find({'task_id': task_id}, {'_id': 0}))
        print(task_infos)
        group_list = set()
        res_score = []
        for i in task_infos:
            group_list.add(i['group_id'])
        length = len(group_list)
        for i in range(1, length + 1):
            print(i)
            s = [x['scores'] for x in task_infos if x['group_id'] == i]
            len_people = len(s)
            len_videos = len(task_infos[0]['scores'])
            print(s, len_people)
            res = [0 for i in range(len_videos)]
            for i in range(len_videos):
                for n in range(len_people):
                    res[i] += s[n][i]
            res = [round(x / len_people, 2) for x in res]
            res_score.append(res)
        score_summary_col = db['rango_tagging_score_summary']
        score_summary_col.insert_one({'task_id': task_id, 'scores': res_score})
        return res_score


class EvaluationDao(object):
    """ 自动评估层数据接口
    """

    def __init__(self, task_id=None):
        """ 数据初始化
        """
        self.__task_id = task_id
        self.task_type_list = self.__get_task_type()
        self.task_boss_url_list = self.__get_task_videos_boss_url()

    def __get_task_type(self):
        """ 获取需要检测的任务类型
        :return:
        """
        return []

    def __get_task_videos_boss_url(self):
        """ 获取task下所有的视频链接
        :return:
        """
        return []

    def __single_video_result(self):
        """
        :return:
        """

    def get_task_result(self):
        """ 获取该任务的自动检测结果，唯一提供的外部接口
        :return:
        """
