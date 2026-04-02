from celery import Celery

celery_app = Celery("test_fastapi_queue")

celery_app.config_from_object("app.queue.celery_config")

if __name__ == '__main__':
    celery_app.start()
