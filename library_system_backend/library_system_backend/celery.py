
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system_backend.settings')

app = Celery('library_system_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Asia/Kuala_Lumpur'

app.autodiscover_tasks()