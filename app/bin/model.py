""" 数据结构定义, 只存放数据
"""
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum, unique

from app.common.data import ReturnCode


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
    tagging_type: TagTypes
    file_list: list  # 二维数组，包含一次任务的所有数据对


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
    group_result: List[TaggingTaskGroupScore]

# ########################## evaluation 模块数据定义 ###########################





