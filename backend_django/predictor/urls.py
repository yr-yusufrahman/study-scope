from django.urls import path, include
from .views import getQuiz, saveResults


urlpatterns = [
    path("get-quiz", getQuiz),
    path("save-results", saveResults),
]
