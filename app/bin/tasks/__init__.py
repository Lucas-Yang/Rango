from celery import Celery
from config.config import CeleryConfig

celery_app = Celery('rango-tasks')
celery_app.config_from_object(CeleryConfig)
