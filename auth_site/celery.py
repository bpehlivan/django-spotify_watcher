from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_site.settings')

app = Celery('auth_site')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-31-seconds': {
        'task': 'spotify_app.tasks.call_refresh_token',
        'schedule': 100.0
    },
    'add-every-30-seconds': {
        'task': 'spotify_app.tasks.get_songs',
        'schedule': 10.0
    },
}
app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))