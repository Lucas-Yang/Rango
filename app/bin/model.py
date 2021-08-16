import json

from datetime import datetime, timezone
from typing import Optional, List, ByteString
from pydantic import BaseModel, Field, BaseConfig
from enum import Enum, unique
from fastapi import UploadFile, File

from app.common.data import ReturnCode

""" 数据结构定义, 只存放数据
"""


@unique
class TagTypes(Enum):
    """ 错误码枚举
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
    """
    task_id: str
    task_name: str
    user: str
    task_type: str
    questionnaire_num: int
    expire_data: Optional[datetime]


class TaggingTaskUpdate(BaseModel):
    """ 标注任务模块- 修改任务
    """
    task_id: str
    task_name: Optional[str]
    questionnaire_num: Optional[int]
    expire_data: Optional[datetime]
    status: Optional[int]


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


# class JobInfo(BaseModel):
#     """
#     created_at 创建日期
#     updated_at 修改日期
#     job_id 任务标识 唯一主键
#     job_name 任务描述
#     job_type  任务类型  标注,指标
#     tasks  视频列表
#     questionnaire_num 评估问卷数量
#     collected_questionnaire_num  已收集的问卷数量
#     expire_data 评估有效期
#     """
#     created_at: Optional[datetime] = Field(None, alias="createdAt")
#     updated_at: Optional[datetime] = Field(None, alias="updatedAt")
#     job_id: ByteString = Field(None)
#     job_name: ByteString
#     job_desc: ByteString
#     job_type: ByteString
#     tasks: List
#     questionnaire_num: int
#     collected_questionnaire_num: int
#     expire_data: Optional[datetime]


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
    FREEZE = 0
    DEFINITION = 1
    NIQE = 2
    BRISQUE = 3


@unique
class VideoEvaluationType(Enum):
    """ 全参考/无参考
    """
    FR = 0
    NR = 1


class EvaluationTaskDetail(BaseModel):
    """ 评估任务task 详情
    """
    index: List[str]
    index_type: int


class EvaluationTaskCreate(TaggingTaskCreate):
    """ 标注任务模块- 创建任务
    """
    task_details: Optional[EvaluationTaskDetail]






