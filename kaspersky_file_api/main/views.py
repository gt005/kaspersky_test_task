from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .api_addons.search_handlers import make_async_searcher

from .models import Search


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


class GetSearchStatusAndPathsAPIView(APIView):
    """ При получении GET запроса возвращает статус поиска с заданным search_id
        и список всех путей к файлам, удовлетворяющих заданным параметрам если
        поиск завершен.
    """

    def get(self, request, search_tag):
        # получаем объект поиска
        try:
            search_task_object = Search.objects.get(tag=search_tag)
        except Search.DoesNotExist:
            return Response(
                {'error': 'search object does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        search_response = {
            'finished': search_task_object.finished,
        }
        if search_task_object.finished:
            search_response['paths'] = [
                path.path for path in search_task_object.paths.all()
            ]

        # возвращаем ответ
        return Response(
            search_response,
            status=status.HTTP_200_OK
        )
