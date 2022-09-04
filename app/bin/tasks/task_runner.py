"""
# 任务队列v2. 抛弃celery,基于databus重新开发
"""

import time
import json
from app.common.databus import Redis


def task_consumer():
    """
    :return:
    """
    sub_rc = Redis(host='bat-shylf-databus.xxx.co',
                   port=6205,
                   auth='0e3f30683b9a83d9:'
                        '9d1250ee4970455c3f66b97947d2f42e@'
                        'RangoJob-bat-TestEp-S/topic=RangoJob-bat-T&role=sub'
                   )
    while True:
        items = sub_rc.get(20)
        print(items)
        if not items:
            continue
        else:
            for item in items:
                ret = json.loads(item)
                print(ret)
                sub_rc.set(ret['partition'], ret['offset'])


if __name__ == "__main__":
    task_consumer()
