from celery import Celery
import os
import conrtollers.qr_controller as qr


broker = os.environ.get('BROKER_URL')
celery_app = Celery('tasks', broker=broker)

@celery_app.task()
def qr_tasks(id: int):
    qr.proceed_order(id)    

