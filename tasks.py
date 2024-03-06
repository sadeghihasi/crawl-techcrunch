# tasks.py

import subprocess

from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def run_main_script():
    # Run the main script using subprocess
    subprocess.run(['python', 'main.py'])
