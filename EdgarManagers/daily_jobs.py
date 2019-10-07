from celery.schedules import crontab
from tasks import app

app.conf.beat_schedule = {
    # Executes every workday at 11 pm.
    'add-every-workday': {
        'task': 'tasks.daily_job',
        'schedule': crontab(hour=23, minute=00, day_of_week='1-5'),
    },
}

app.conf.timezone = 'US/Pacific'

# celery -A daily_jobs beat --loglevel=info