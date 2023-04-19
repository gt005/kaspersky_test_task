import os

from django.core.wsgi import get_wsgi_application
from rq import Worker, Queue, Connection
from redis import Redis

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaspersky_file_api.settings')
_application = get_wsgi_application()

redis_conn = Redis(host=REDIS_HOST)

with Connection(redis_conn):
    qs = [Queue(connection=redis_conn)]
    w = Worker(qs)
    w.work()
