from django.urls import path, include

from .views import CreateSearchAPIView, GetSearchStatusAndPathsAPIView

urlpatterns = [
    path('search', CreateSearchAPIView.as_view(), name='create_search_api_view'),
    path('searches/<search_tag>', GetSearchStatusAndPathsAPIView.as_view(), name='get_search_status_and_paths_api_view'),
]