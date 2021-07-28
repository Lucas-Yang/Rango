""" 为接口生产数据
"""


class TaggingDao(object):
    """
    """


class EvaluationDao(object):
    """ 自动评估层数据接口
    """
    def __init__(self, task_id=None):
        """ 数据初始化
        """
        self.__task_id = task_id

    def test(self):
        """
        :return:
        """
        pass
