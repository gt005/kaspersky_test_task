from time import sleep
from uuid import uuid4

import os

from redis import Redis
from rq import Queue
from rq.job import Job

from ..models import Search

q = Queue(connection=Redis(host=os.getenv('REDIS_HOST', 'localhost')))


def make_search(create_request: dict) -> list[str]:
    """ Выполняет поиск файлов по заданным параметрам

    :param create_request: Параметры, заданные условием задачи
    :return: Список всех путей к файлам, удовлетворяющих заданным параметрам
    """
    sleep(5)

    return [
        'test_path_1/' + str(uuid4()),
        'test_path_2/' + str(uuid4()),
        'test_path_3/' + str(uuid4()),
    ]


def add_paths_to_db_and_finish_search(job: Job, connection, result: list[str],
                                      *args, **kwargs) -> None:
    """
        Предназначен для вызова в качетсве on_success callback redis.
        Вызывается после завершения поиска файлов по заданным параметрам.
        Сохраняет результат в БД и изменяет статус поиска на "завершен".

    :param job: Объект задачи, созданной Redis
    :param result: Результат выполнения задачи поиска файлов
    """

    try:
        search_task_object = Search.objects.get(tag=str(job.id))
    except Search.DoesNotExist:
        print("Search object does not exist")
        return

    for path in result:
        search_task_object.paths.create(path=path).save()


def make_async_searcher(create_request: dict) -> 'Job':
    """ Создает объект поиска и запускает асинхронный поиск файлов по заданным
        параметрам
    :param create_request: Параметры, заданные условием задачи
    :return: Объект задачи
    """
    # Запускаем асинхронный поиск файлов по параметрам и после завершения
    # сохраняем результат в БД и изменяем статус поиска на "завершен"
    result = q.enqueue(
        make_search,
        create_request,
        on_success=add_paths_to_db_and_finish_search
    )

    if result:
        Search(tag=str(result.id)).save()

    return result
