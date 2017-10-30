import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'review_site.settings')

app = Celery('review_site')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()