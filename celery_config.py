from tasks import app  # Import the app instance from tasks.py

app.conf.beat_schedule = {
    'check-gps-every-minute': {
        'task': 'tasks.check_gps_and_send_email',
        'schedule': crontab(minute='*'),
    },
}
