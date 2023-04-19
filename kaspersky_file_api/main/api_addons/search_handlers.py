from time import sleep
from uuid import uuid4

from redis import Redis
from rq import Queue

from ..models import Search


q = Queue(connection=Redis())


def make_search(create_request: dict) -> str:
    """ Создает асинхронный поисковый запрос, запускает его и возвращает его
    идентификатор."""
    Search(
        tag=str(uuid4())
    ).save()
    sleep(10)
    Search(
        tag=str(uuid4())
    ).save()


def make_async_searcher(create_request: dict):
    result = q.enqueue(make_search, create_request)
    print(result.id)
    return result