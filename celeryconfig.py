from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

# Define the periodic task
app.conf.beat_schedule = {
    'run-main-script': {
        'task': 'tasks.run_main_script',
        'schedule': 86400,  # 24 hours in seconds
    },
}

app.conf.timezone = 'UTC'
