from django.urls import path, include
from .views import all_courses, change_courses


urlpatterns = [
    path("get", all_courses),
    path("change", change_courses),
]
