# 存放自定义的数据结构
from pydantic import BaseModel

# ########################## 通用错误码定义 ###########################


class ErrorCode(object):
    """
    """

    def __init__(self):
        pass


# ########################## bin 模块数据定义 ###########################
# 标注任务模块

# 评估任务模块

# ########################## user 模块数据定义 ###########################

class UserLoginItem(BaseModel):
    """ 用户模块-登陆数据
    """
    email: str
    password: str
