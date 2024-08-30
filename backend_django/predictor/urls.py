from django.urls import path, include
from .views import getQuiz, saveResults, getTree, dataTest


urlpatterns = [
    path("get-quiz", getQuiz),
    path("save-results", saveResults),

    # Test purposes...
    path("get-tree", getTree),
    path("test-tree", dataTest),
]
