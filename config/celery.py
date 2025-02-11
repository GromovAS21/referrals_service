from __future__ import absolute_import
import os
from celery import Celery

from config.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery("config")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = CELERY_BROKER_URL
app.conf.result_backend = CELERY_RESULT_BACKEND
app.autodiscover_tasks()
