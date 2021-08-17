import json

from datetime import datetime, timezone
from typing import Optional, List, ByteString
from pydantic import BaseModel, Field, BaseConfig
from enum import Enum, unique

from app.common.data import ReturnCode

""" 数据结构定义, 只存放数据
"""


@unique
class TagTypes(Enum):
    """
    """
    SINGLE_TYPE = 0  # 无参考标注
    DOUBLE_TYPE = 1  # 有参考视频标注


class BinModelReturn(BaseModel):
    """ 主业务模块 - 返回值
    """
    code: ReturnCode
    msg: str
    data: Optional[dict]


# ########################## tag 模块数据定义 ###########################


class TaggingTaskCreate(BaseModel):
    """ 标注任务模块- 创建任务

    task_id: 任务id（唯一)

    task_name: 任务名字

    user: 创建人

    task_type: 任务类型，tagging(标注) / evaluation(自动评估)

    questionnaire_num: 收集样本量

    expire_data: 过期时间

    """
    task_id: str
    task_name: str
    user: str
    task_type: str
    questionnaire_num: int
    expire_data: Optional[datetime]


class TaggingTaskUpdate(BaseModel):
    """ 标注任务模块 - 修改任务

    task_id: 任务id（唯一)

    task_name: 任务名字

    questionnaire_num: 收集样本量

    expire_data: 过期时间

    status: 是否可标注
    """
    task_id: str
    task_name: Optional[str]  # 任务名字
    questionnaire_num: Optional[int]
    expire_data: Optional[datetime]
    status: Optional[int]


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


class TaggingTaskStatus(BaseModel):
    """ 标注任务模块 - 总查询任务接口
    """
    page_size: int
    page_num: int


class TaggingTaskGroupScore(BaseModel):
    """ 标注任务模块 - 打分回收接口 子数据结构
    """
    group_id: int
    group_score: int


class TaggingTaskScore(BaseModel):
    """ 标注任务模块 - 打分回收接口

    task_id: 任务id

    group_id: 任务-文件组id

    scores: 组内每个文件的分数

    user: 打分人id
    """
    task_id: str
    group_id: int
    scores: List[int]
    user: str


class UserTaskStatus(BaseModel):
    """ 用户完成任务状态
    """
    task_id: str
    status: str
    user: str

# ########################## evaluation 模块数据定义 ###########################


@unique
class VideoEvaluationFRIndex(Enum):
    """ 视频全参考指标
    """
    SSIM = 0
    PSNR = 1
    VMAF = 2


@unique
class VideoEvaluationNRIndex(Enum):
    """ 视频无参考指标
    """
    DEFINITION = 0
    NIQE = 1
    BRISQUE = 2


@unique
class VideoEvaluationType(Enum):
    """ 全参考/无参考

    FR: 0  # 全参考(两个视频)

    NR: 1  # 无参考(单个视频)
    """
    FR = 0
    NR = 1


class EvaluationTaskDetail(BaseModel):
    """ 评估任务task 详情

    index: 具体的指标(全参考：{SSIM = 0， PSNR = 1， VMAF = 2}
    无参考： { DEFINITION = 0, NIQE = 1, BRISQUE = 2}

    index_type: 指标类型
    """
    index: List[int]
    index_type: VideoEvaluationType


class EvaluationTaskCreate(TaggingTaskCreate):
    """ 评估任务模块 - 创建任务
    """
    task_details: Optional[EvaluationTaskDetail]






