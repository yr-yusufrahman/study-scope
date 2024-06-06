from django.shortcuts import render

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from random import shuffle

from predictor.helpers.mcq import createQuiz

#from courses.models import Card


# Create a quiz with cards from a given chapter
@api_view(["POST"])
def getQuiz(request):
    # First confirm if user access token is valid
    user = request.user
    if user:
        # Get the chapter id
        #chapter_id = request.data.get('chapter_id')
        #cards = Card.objects.filter(chapter=chapter_id).order_by('order')
        cards = request.data.get('cards')
        shuffle(cards)

        # Create a quiz with the cards - Array of dictionaries {mutliple_choice, blanked, options}
        quiz = createQuiz(cards)

        return Response(quiz, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_401_UNAUTHORIZED)