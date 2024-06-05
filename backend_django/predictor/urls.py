from django.urls import path, include
from .views import getQuiz


urlpatterns = [
    path("get-quiz", getQuiz),

]
