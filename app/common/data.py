""" 所有app 共用 数据
"""
from enum import Enum, unique


# ########################## 通用错误码定义 ###########################

@unique
class ReturnCode(Enum):
    """ 错误码枚举
    """
    SUCCESS = 0  # 成功
    INPUT_ERROR = 1  # 输入错误
    INTERNAL_ERROR = 2  # 内部错误
    SQL_ERROR = 3  # sql 错误
    UNKNOWN_ERROR = 4  # 未知错误


if __name__ == '__main__':
    pass
