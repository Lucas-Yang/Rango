""" 数据结构定义, 只存放数据
"""
from datetime import datetime, timezone
from typing import Optional,List,ByteString
from pydantic import BaseModel, Field, BaseConfig
import json


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
