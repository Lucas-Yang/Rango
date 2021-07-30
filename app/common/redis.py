import time
import uuid

import redis
import smtplib
from email.mime.text import MIMEText
from email.header import Header

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

sender = '396937118@qq.com'
password = 'mvejgvmefnerbhjb'

# 发信服务器
smtp_server = 'smtp.qq.com'

class RedisClient:
    """
    Redis 操作类
    """

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        """init
        :param host:
        :param port:
        """
        self.host = host
        self.port = port

    def create_verification_code(self, email):
        temp = uuid.uuid4()
        v_code = str(temp).replace('-', '')[:6]
        r = redis.Redis(host=self.host, port=self.port, db=0)
        # 存储数据库
        r.set(email, v_code, ex=60)

        # 发送邮件
        receiver = email
        body = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html";charset="utf-8">
        <title>verification code email</title>
        </head>
        <body>
        <p>本次注册的验证码:</p>
        <p><h1>{}</h1></p>
        </body>
        </html>
        """
        message = MIMEText(body.format(v_code), 'html', 'utf-8')
        message['From'] = Header(sender)
        message['To'] = Header(receiver)
        message['Subject'] = Header('rango 注册验证码', 'utf-8')

        try:
            server = smtplib.SMTP_SSL(smtp_server)
            server.connect(smtp_server, 465)
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
            server.close()
            return True, "验证码发送成功"
        except smtplib.SMTPException:
            return False, "邮件发送失败"

    def get_verification_code(self, email):
        r = redis.Redis(host=self.host, port=self.port, db=0)
        # 读取验证码
        v_code = r.get(email)
        return v_code
