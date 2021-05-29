from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube.settings')

app = Celery('youtube')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "fetch_youtube_videos": {
        "task": "fetch_youtube_videos",
        "schedule": crontab(minute=f"*/{settings.TASK_FREQUENCY}"),
    },
}
app.conf.timezone = settings.CELERY_TIMEZONE


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
