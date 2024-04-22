from django.urls import path, include
from .views import all_courses


urlpatterns = [
    path("get", all_courses),
]
