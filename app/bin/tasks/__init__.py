from celery import Celery
from config.config import CeleryConfig

celery_app = Celery('rango-tasks',
                    broker=CeleryConfig.broker_url,
                    backend=CeleryConfig.backend,
                    include=["app.bin.tasks.evaluation_task"]
                    )
# celery_app.config_from_object(CeleryConfig)
