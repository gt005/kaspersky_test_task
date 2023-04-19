from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .api_addons.search_handlers import make_async_searcher


class CreateSearchAPIView(APIView):
    """ При получении POST запроса создает объект поиска и запускает асинхронный
        поиск файлов по заданным в post запросе json параметрам
    """

    def post(self, request):

        # запускаем асинхронный поиск файлов по параметрам и после завершения
        # сохраняем результат в БД и изменяем статус поиска на "завершен"
        job = make_async_searcher(request.data)

        # возвращаем ответ
        if job:
            return Response({'search_id': str(job.id)},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'search_id': 'error while creating search object'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
