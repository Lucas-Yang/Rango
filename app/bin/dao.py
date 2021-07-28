""" 为接口生产数据
"""
from app.bin.utils.Evaluation import FRVideoEvaluationFactory
from app.bin.utils.Evaluation import NRVideoEvaluationFactory


class TaggingDao(object):
    """ 数据标准层数据接口
    """


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
