from django.urls import path, include
from .views import getCourses, changeCourses, getChapters, getCards, changeCards


urlpatterns = [
    path("get-courses", getCourses),
    path("change-courses", changeCourses),
    path("get-chapters", getChapters),
    path("get-cards", getCards),
    path("change-cards", changeCards)
]
