import app.bin.model as model
from app.common.db import MyMongoClient
from app.common import mongodb_client
import time
from datetime import datetime
# from app.bin.utils.Evaluation import FRVideoEvaluationFactory
# from app.bin.utils.Evaluation import NRVideoEvaluationFactory
""" 为接口生产数据
"""


class TaggingDao(object):
    """

    数据标准层数据接口
    """

    def __init__(self):
        self.db = mongodb_client

    def query_tagging_task(self, task_id):
        task_col = self.db['rango_evaluate_tasks']
        res = task_col.find_one({'task_id': task_id}, {'_id': 0})
        return res

    def query_tagging_task_by_index(self, task_id, index):
        task_col = self.db['rango_evaluate_tasks']
        res = task_col.find_one({'task_id': task_id}, {'groups': 1})
        res = res.get('groups')
        res = res.get(str(index)) if res.get(str(index)) else []
        return res

    def query_tagging_task_by_user(self, user, skip, limit_num):
        """ 获取所有的待标注任务
        todo  添加status
        :param:
        :return:
        """
        task_col = self.db['rango_evaluate_tasks']

        if not user:
            user = {'$regex': '.*'}
        if user == 'all':
            user = {'$regex': '.*'}
        skip = (skip - 1) * limit_num
        count = len(list(task_col.find({'user': user,'task_type':'tagging','status':0})))
        res = list(task_col.find({'user': user,'task_type':'tagging','status':0}, {'_id': 0}).sort([("created_at", -1)]).skip(skip).limit(limit_num))
        return res, count

    def delete_tagging_task(self, task_id):
        task_col = self.db['rango_evaluate_tasks']
        res = task_col.delete_one({'task_id': task_id})
        return res.deleted_count

    def modify_tagging_task(self, query: model.TaggingTaskUpdate):
        task_col = self.db['rango_evaluate_tasks']
        user_col = self.db['rango_tagging_users']
        update = {'updated_at': time.strftime("%Y-%m-%d %H:%M:%S")}
        update_users = {'updated_at': time.strftime("%Y-%m-%d %H:%M:%S")}

        if query.task_name:
            update['job_name'] = query.task_name

        if query.questionnaire_num:
            update['questionnaire_num'] = query.questionnaire_num

        if query.expire_data:
            update['expire_data'] = query.expire_data
            update_users['expire_data'] = query.expire_data

        if query.status:
            update['status'] = query.status
            update_users['status'] = query.status

        select = {'task_id': query.task_id}
        update = {"$set": update}
        update_users = {"$set": update_users}

        res = task_col.update_one(select, update)
        res2 = user_col.update_one(select, update_users)

        return res.modified_count

    def delete_upload_file(self, fid):
        file_col = self.db['rango_task_files']
        res = file_col.delete_one({'fid': fid})
        return res.deleted_count

    def query_upload_file_by_task_id(self, task_id):
        file_col = self.db['rango_task_files']
        res = list(file_col.find({'task_id': task_id}, {'_id': 0}).sort([("group_id", -1)]))
        return res

    def collect_video_task_score(self, score_info: dict):
        score_col = self.db['rango_tagging_score']
        res = score_col.insert_one(score_info)
        return res

    def record_tagging_task_user(self, tasks_info: dict):
        task_col = self.db['rango_evaluate_tasks']
        task_info = task_col.find_one({'task_id': tasks_info['task_id']},
                                      {'task_name': 1, 'expire_data': 1})
        print('task_info',task_info)
        score_col = self.db['rango_tagging_users']
        select = {'task_id': tasks_info['task_id'], 'user': tasks_info['user']}
        update_set = {"$set": {'task_id': tasks_info['task_id'], 'task_name': task_info['task_name'],
                               'expire_data': task_info['expire_data'].strftime("%Y-%m-%d %H:%M:%S"),
                               'user': tasks_info['user'], 'status': tasks_info['status'],
                               'created_at': time.strftime("%Y-%m-%d %H:%M:%S")}}
        res = score_col.update_one(select, update_set, upsert=True)
        return res

    def video_query_user_task(self, user, skip, limit_num):
        score_col = self.db['rango_tagging_users']
        skip = (skip - 1) * limit_num
        count = len(list(score_col.find({'user': user})))
        res = list(score_col.find({'user': user}, {'_id': 0}).sort([("created_at", -1)]).skip(skip).limit(limit_num))
        return res, count

    def video_query_task_score(self, task_id: str):
        score_col = self.db['rango_tagging_score_summary']
        res = score_col.find_one({'task_id': task_id}, {'scores': 1, '_id': 0})
        return res

    def computed_video_task_scores(self, task_id):
        score_col = self.db['rango_tagging_score']
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
        score_summary_col = self.db['rango_tagging_score_summary']
        score_summary_col.insert_one({'task_id': task_id, 'scores': res_score})
        return res_score


class EvaluationDao(object):
    """ 自动评估层数据接口
    """

    def __init__(self, task_id=None):
        """ 数据初始化
        """
        self.__mongodb_client = mongodb_client
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

    def __search_collection_result(self, collection_name: str, search_info_dict: dict):
        """
        :param collection_name:
        :param search_info_dict:
        :return:
        """
        evaluation_task_result_collection = self.__mongodb_client[collection_name]
        task_result_iter = evaluation_task_result_collection.find(search_info_dict)
        return task_result_iter

    def delete_evaluation_task(self, user_id, task_id):
        """ 删除用户评估任务
        :return:
        """
        evaluation_task_collection = self.__mongodb_client["rango_evaluate_tasks"]
        evaluation_task_collection.delete_one({"task_id": task_id, "user": user_id})

    def get_task_personal_result(self, user_id):
        """ 获取该任务的自动检测结果，唯一提供的外部接口
        :return:
        """
        task_result_iter = self.__search_collection_result(
            collection_name="rango_evaluation_task_result",
            search_info_dict={'user': user_id}
        )
        task_create_iter = self.__search_collection_result(
            collection_name="rango_evaluate_tasks",
            search_info_dict={"user": user_id, "task_type": "evaluation"}
        )
        create_list = [{
            "task_id": data["task_id"],
            "task_name": data["task_name"],
            "index_type": data.get("task_detail", {"index_type": 2}).get("index_type"),
            "groups": data["groups"]
        }
            for data in task_create_iter
        ]
        result_list = [{
            "task_id": data["task_id"],
            "evaluation_result": data["task_evaluation_result"]
        }
            for data in task_result_iter
        ]
        for index, create_data in enumerate(create_list):
            for result_data in result_list:
                if create_data["task_id"] == result_data["task_id"]:
                    create_data["evaluation_result"] = result_data["evaluation_result"]
        return create_list


if __name__ == '__main__':
    evaluate_client = EvaluationDao()
    personal_task_info = evaluate_client.get_task_personal_result('lukkk')
    print(personal_task_info)
