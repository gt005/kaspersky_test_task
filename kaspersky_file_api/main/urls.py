from django.urls import path, include

from .views import CreateSearchAPIView

urlpatterns = [
    path('search', CreateSearchAPIView.as_view()),
]