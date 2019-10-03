from tasks import app
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.test_log_time',
        'schedule': 30.0
    },
}
app.conf.timezone = 'US/Pacific'