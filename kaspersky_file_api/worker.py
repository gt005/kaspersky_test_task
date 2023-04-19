import os

from django.core.wsgi import get_wsgi_application
from rq import Worker, Queue, Connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaspersky_file_api.settings')
_application = get_wsgi_application()

with Connection():
    qs = [Queue()]
    w = Worker(qs)
    w.work()
