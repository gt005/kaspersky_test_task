from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from time import sleep

from .api_addons.search_handlers import make_async_searcher


class CreateSearchAPIView(APIView):
    def post(self, request):
        job = make_async_searcher(request.data)

        # возвращаем ответ
        if job:
            return Response({'message': 'Задача добавлена в очередь'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'message': 'Не удалось добавить задачу в очередь'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
