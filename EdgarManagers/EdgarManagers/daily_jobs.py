from datetime import datetime
from celery.schedules import crontab
import sys
sys.path.append("..")
from tasks import app
from config import local_timezone

app.conf.beat_schedule = {
    # Executes every workday at 11 pm.
    'add-every-workday': {
        'task': 'tasks.daily_job',
        'schedule': crontab(hour=23, minute=00, day_of_week='1-5'),
        'args': local_timezone.localize(datetime.today()).strftime('%Y%m%d')
    },
}

app.conf.timezone = 'US/Pacific'

# celery -A daily_jobs beat --loglevel=info