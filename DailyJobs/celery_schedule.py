from celery.schedules import crontab
from tasks import app

app.conf.beat_schedule = {
    # Executes every workday at 11 pm.
    'add-every-workday': {
        'task': 'tasks.daily_job',
        'schedule': crontab(hour=23, minute=00, day_of_week='mon, tue, wed, thu,fri'),
    },
}

app.conf.timezone = 'US/Pacific'

# celery -A test_celery_schedule beat --loglevel=info