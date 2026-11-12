from django.shortcuts import render

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from random import shuffle
from datetime import datetime

from predictor.models import Revision
from courses.models import Course, Chapter
#from predictor.helpers.mcq import createQuiz
from predictor.helpers.createQuiz import createQuiz
#from predictor.helpers.loadModel import queryModel
from predictor.helpers.makePrediction import makePrediction


# Create a quiz with cards from a given chapter
@api_view(["POST"])
def getQuiz(request):
    # First confirm if user access token is valid
    user = request.user
    if user.is_authenticated:
        # Get the chapter id
        #cards = Card.objects.filter(chapter=chapter_id).order_by('order')
        course_name = request.data.get('course_name') or ''
        cards = request.data.get('cards') or []
        if not cards:
            return Response(
                {'error': 'No flashcards in this chapter to quiz.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        shuffle(cards)

        try:
            # Returns {quiz_content, total, history}
            quiz_dictionary = createQuiz(cards, course_name)
        except Exception:
            return Response(
                {'error': 'Quiz could not be generated.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(quiz_dictionary, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_401_UNAUTHORIZED)


# Save results of a quiz
@api_view(["POST"])
def saveResults(request):
    # First confirm if user access token is valid
    user = request.user
    if user.is_authenticated:
        # Get the results
        mistakes = request.data.get('mistakes')
        inputs = request.data.get('inputs')
        #number_of_reveals = request.data.get('number_of_reveals')
        chapter_id = request.data.get('chapter_id')
        course_id = request.data.get('course_id')

        chapter = Chapter.objects.filter(id=chapter_id, course__owner=user).first()
        if chapter and inputs > 0:
            # Check if the chapter already had a previous revision on the same date
            last_revision = Revision.objects.filter(chapter=chapter).order_by('-date').first()

            # Check if the revision was on the same day
            if last_revision:
                if last_revision.date.date() == datetime.now().date():
                    # Make no changes
                    return Response(status=status.HTTP_200_OK)
                
            #percentage_of_reveals = (number_of_reveals / inputs) * 100
            #percentage_of_reveals = round(percentage_of_reveals, 2)

            # Save the results
            revision = Revision.objects.create(
                mistakes=mistakes,
                inputs=inputs,
                chapter=chapter
            )
            revision.save()
            revision.setDaysSince() # Calculate the days since last revision
            revision.complete() # Calculate the other field values from last revision data point
            
            # If drop-off was detected, retrain the tree

            # Make a prediction
            course = Course.objects.filter(id=course_id, owner=user).first()
            if not course:
                return Response(status=status.HTTP_404_NOT_FOUND)
            prediction = makePrediction(revision, user)
            chapter.setDue(prediction) # Set the next due date for the chapter

            # Save successful
            return Response(status=status.HTTP_200_OK)

        # Chapter not found
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # User not authenticated
    return Response(status=status.HTTP_401_UNAUTHORIZED)


# To get a prediction, just get the value from the next_due field in the Chapter model
