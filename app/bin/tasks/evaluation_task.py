from app.bin.tasks import celery_app


@celery_app.task
def test_task(x, y):
    """
    :return:
    """
    return x + y


if __name__ == '__main__':
    celery_app.worker_main()



