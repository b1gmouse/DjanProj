import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add_every_morning': {
        'task': 'news.tasks.get_news',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
    'clear_board_every_evening_morning': {
        'task': 'news.tasks.clear_old',
        'schedule': crontab(hour=23, minute=0, day_of_week='monday'),
    },
    'new_post': {
        'task': 'news.tasks.notify_subscribers',
        'schedule': crontab(),
        'args': (5, 4)
    },
}


