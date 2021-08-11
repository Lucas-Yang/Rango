# mysql 和 fuzz 共用了一套数据库, asko proxy: fuzz
mysql_config = {
    "host": "127.0.0.1",
    "username": "rango",
    "password": "zIqRppohJafxRp9LHlKbPN7PAMmNhH4Z",
    "database": "rango",
    "port": 3306
}

# mongo
mongo_config = {
    "mongodb_user": "mobileautotest",
    "mongodb_password": "baYeDMOQB1vNE3losdFLfVg5Rr7ACZph",
    "mongodb_uri": "mongodb://172.22.34.101:3301,172.22.34.102:3301"
}

# redis overload proxy: rango
redis_config = {
    "host": "127.0.0.1",
    "port": 26891
}


# email
email_config = {
    "sender": '396937118@qq.com',
    "password": 'mvejgvmefnerbhjb',
    "smtp_server": 'smtp.qq.com'
}

# celery
# celery 任务队列, mongodb 作为backend方便持久化存储


class CeleryConfig:
    broker_url = 'redis://0.0.0.0:6379/3'
    backend = 'redis://0.0.0.0:6379/4'
    task_track_started = True
    enable_utc = True
    timezone = 'Asia/Shanghai'
    """
    broker_url = 'redis://0.0.0.0:6379/3'
    task_track_started = True
    result_backend = 'mongodb://burytest:GbnO35lpzAyjkPqSXQTiHwLuDs2r4gcR@172.22.34.102:3301/test' \
                            '?authSource=burytest&replicaSet=bapi&readPreference=primary&appname=MongoDB%2' \
                            '0Compass&ssl=false'
    mongodb_backend_settings = {
        "database": "burytest",
        "taskmeta_collection": "rango"
    }
    """