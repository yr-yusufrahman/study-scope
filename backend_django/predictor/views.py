from django.shortcuts import render

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from random import shuffle
from datetime import datetime

from predictor.models import Revision
from courses.models import Chapter, Card

from predictor.helpers.mcq import createQuiz


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
        quiz = createQuiz(cards) # Returns {quiz_content, total, history}

        return Response(quiz, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_401_UNAUTHORIZED)


# Save results of a quiz
@api_view(["POST"])
def saveResults(request):
    # First confirm if user access token is valid
    user = request.user
    if user:
        # Get the results
        mistakes = request.data.get('mistakes')
        inputs = request.data.get('inputs')
        number_of_reveals = request.data.get('number_of_reveals')
        chapter_id = request.data.get('chapter_id')

        chapter = Chapter.objects.get(id=chapter_id)
        if chapter:
            # Check if the chapter already had a previous revision on the same date
            last_revision = Revision.objects.filter(chapter=chapter).order_by('-date').first()

            # Check if the revision was on the same day
            if last_revision:
                if last_revision.date.date() == datetime.now().date():
                    # Make no changes
                    return Response(status=status.HTTP_200_OK)
                

            # Save the results
            revision = Revision.objects.create(
                mistakes=mistakes,
                inputs=inputs,
                number_of_reveals=number_of_reveals,
                chapter=chapter
            )
            revision.save()

            # Save successful
            return Response(status=status.HTTP_200_OK)

        # Chapter not found
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # User not authenticated
    return Response(status=status.HTTP_401_UNAUTHORIZED)