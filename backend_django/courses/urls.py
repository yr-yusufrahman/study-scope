from django.urls import path, include
from .views import getCourses, changeCourses, getCards


urlpatterns = [
    path("get", getCourses),
    path("change", changeCourses),
    path("cards", getCards),
]
