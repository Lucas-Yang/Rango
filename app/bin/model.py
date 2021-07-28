from datetime import datetime, timezone
from typing import Optional,List,ByteString
from pydantic import BaseModel, Field, BaseConfig
import json
from enum import Enum, unique

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


class TaggingTaskCreate(BaseModel):
    """ 标注任务模块- 创建任务
    """
    tagging_type: TagTypes
    file_list: list  # 二维数组，包含一次任务的所有数据对

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)


class JobInfo(BaseModel):
    """
    created_at 创建日期
    updated_at 修改日期
    job_id 任务标识 唯一主键
    job_name 任务描述
    job_type  任务类型  标注,指标
    tasks  视频列表
    questionnaire_num 评估问卷数量
    collected_questionnaire_num  已收集的问卷数量
    expire_data 评估有效期
    """
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    job_id:ByteString = Field(None)
    job_name:ByteString
    job_desc:ByteString
    job_type:ByteString
    tasks:List
    questionnaire_num:int
    collected_questionnaire_num:int
    expire_data:Optional[datetime]