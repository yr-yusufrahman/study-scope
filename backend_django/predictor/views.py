from django.shortcuts import render

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from random import shuffle
from datetime import datetime
import os
import joblib, pickle
from sklearn.preprocessing import StandardScaler
import numpy as np

from predictor.models import Revision, Predictor
from courses.models import Course, Chapter, Card
from predictor.helpers.mcq import createQuiz
from predictor.helpers.loadModel import queryModel


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
        course_id = request.data.get('course_id')

        chapter = Chapter.objects.get(id=chapter_id)
        if chapter and inputs > 0:
            # Check if the chapter already had a previous revision on the same date
            last_revision = Revision.objects.filter(chapter=chapter).order_by('-date').first()

            # Check if the revision was on the same day
            if last_revision:
                if last_revision.date.date() == datetime.now().date():
                    # Make no changes
                    return Response(status=status.HTTP_200_OK)
                
            percentage_of_reveals = (number_of_reveals / inputs) * 100
            percentage_of_reveals = round(percentage_of_reveals, 2)

            # Save the results
            revision = Revision.objects.create(
                mistakes=mistakes,
                inputs=inputs,
                percentage_of_reveals=percentage_of_reveals,
                chapter=chapter
            )
            revision.save()
            revision.setDaysSince() # Calculate the days since last revision
            revision.complete() # Calculate the other field values from last revision data point
            

            # Make a prediction
            course = Course.objects.get(id=course_id)
            prediction = makePrediction(revision, course)
            data = {
                'next_due': prediction
            }
            # Save successful
            return Response(data, status=status.HTTP_200_OK)

        # Chapter not found
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # User not authenticated
    return Response(status=status.HTTP_401_UNAUTHORIZED)


# Make a prediction after a quiz
def makePrediction(revision_obj, course_obj):
    days_since = revision_obj.days_since
    mistake_score = (revision_obj.mistakes / revision_obj.inputs) * 100
    mistake_score = round(mistake_score, 4)
    inputs = revision_obj.inputs
    percentage_of_reveals = revision_obj.percentage_of_reveals

    # Prepare the input for the model
    raw_data = np.array([
        [
            days_since,
            mistake_score, 
            inputs, 
            percentage_of_reveals
        ],
    ])
    
    # Get the course model parameters
    predictor = Predictor.objects.get_or_create(course=course_obj)

    params = predictor[0].parameters

    # Make a prediction
    prediction = queryModel(params, raw_data)
    print(f"Prediction: {prediction}\n")
    return prediction


# To get a prediction, just get the value from the next_due field in the Chapter model



# Test purposes...
@api_view(["GET"])
def getTree(request):
    user = request.user
    if user:
        predictor = Predictor.objects.get_or_create(user=user) # Returns a tuple [0] contains obj, [1] boolean success
        print(f"Predictor: {predictor}\n")
        model_serialized = predictor[0].tree
        model = pickle.loads(model_serialized)

        # Strange case test
        more = np.array([[4, 137.5, 10]])
        more_pred = model.predict(more)
        print(f"\nThis should be around 7-12: {more_pred}")


        return Response(status=status.HTTP_200_OK)
    
    # User not authenticated
    return Response(status=status.HTTP_401_UNAUTHORIZED)


