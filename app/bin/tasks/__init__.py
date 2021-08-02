from celery import Celery
from config import testconfig

celery_app = Celery('rango-tasks')
celery_app.config_from_object(testconfig)
