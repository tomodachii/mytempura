from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# from celery.schedules import crontab
from dotenv import load_dotenv

# set the default Django settings module for the 'celery' program.
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

app = Celery("main")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("setup_periodic_tasks")
    # Calls test('world') every 3 seconds
    # sender.add_periodic_task(3.0, test.s('Test beat and Celery'))


@app.task
def test(str):
    print("Testing task: " + str)
    return str
