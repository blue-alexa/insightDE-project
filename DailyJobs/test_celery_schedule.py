from tasks import app
app.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'tasks.test_log_time',
        'schedule': 5.0
    },
}
app.conf.timezone = 'US/Pacific'

# celery -A test_celery_schedule beat --loglevel=info