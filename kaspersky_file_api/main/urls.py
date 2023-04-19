from django.urls import path, include

from .views import CreateSearchAPIView, GetSearchStatusAndPathsAPIView

urlpatterns = [
    path('search', CreateSearchAPIView.as_view()),
    path('searches/<search_tag>', GetSearchStatusAndPathsAPIView.as_view()),
]