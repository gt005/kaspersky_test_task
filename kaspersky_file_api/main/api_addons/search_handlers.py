import os

from redis import Redis
from rq import Queue
from rq.job import Job

from ..models import Search
from .search_functions import make_search

q = Queue(connection=Redis(host=os.getenv('REDIS_HOST', 'localhost')))
ABSOLUTE_PATH_TO_FIND_DIR = os.getenv('ABSOLUTE_PATH_TO_FIND_DIR')


def add_paths_to_db_and_finish_search(job: Job, connection, result: list[str],
                                      *args, **kwargs) -> None:
    """ Предназначен для вызова в качетсве on_success callback redis.
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

    search_task_object.finished = True
    search_task_object.save()


def make_async_searcher(file_find_criteria: dict) -> Job:
    """ Создает объект поиска и запускает асинхронный поиск файлов по заданным
        параметрам
    :param file_find_criteria: Параметры, заданные условием задачи
    :return: Объект задачи
    """
    if ABSOLUTE_PATH_TO_FIND_DIR is None:
        raise ValueError("ABSOLUTE_PATH_TO_FIND_DIR is not set")

    # Запускаем асинхронный поиск файлов по параметрам и после завершения
    # сохраняем результат в БД и изменяем статус поиска на "завершен"
    result = q.enqueue(
        make_search,
        ABSOLUTE_PATH_TO_FIND_DIR,
        file_find_criteria,
        on_success=add_paths_to_db_and_finish_search
    )

    if result:
        Search(tag=str(result.id)).save()

    return result

