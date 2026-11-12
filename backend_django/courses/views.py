from django.shortcuts import render

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime

from .models import Course, Chapter, Card
from predictor.models import Revision
from .helpers.editRequests import editCourses, editChapters, editCards


# ------------------- Get Requests -------------------

# Returns all course data and chapter for a user
@api_view(["GET"])
def getCourses(request):
    # First confirm if user access token is valid
    user = request.user
    if user.is_authenticated:
        # All courses for the user
        courses = Course.objects.filter(owner=user).order_by('title')
        courses_data = []
        for course in courses:
            # All chapters for the course
            #chapters = Chapter.objects.filter(course=course)
            courses_data.append({
                'id': course.id,
                'title': course.title,
                #'chapters': [{
                #    'id': chapter.id,
                #    'title': chapter.chapter_title,
                #} for chapter in chapters],
            })
            
        response = {
            'courses': courses_data,
        }

        return Response(response, status=status.HTTP_200_OK)
    
    bad_response = {
        'error': 'User not authenticated.',
    }
    return Response(bad_response, status=status.HTTP_401_UNAUTHORIZED)


# Returns all chapters for a course
@api_view(["POST"])
def getChapters(request):
    # First confirm if user access token is valid
    user = request.user
    if user.is_authenticated:
        course_id = request.data.get('course_id')
        course = Course.objects.filter(owner=user, id=course_id).first()

        # Check if course exists and belongs to user
        if course:
            # Get all chapters for the course
            chapters = Chapter.objects.filter(course=course).order_by('order')
            chapters_data = []

            for chapter in chapters:
                data = {
                    'id': chapter.id,
                    'title': chapter.chapter_title,
                    'next_due': {},
                    'last_result': {}
                }

                # Check if the chapter has a next due date
                if chapter.next_due:
                    data['next_due'] = {
                        'date': chapter.next_due.strftime('%Y-%m-%d'),
                        'days': (chapter.next_due - timezone.now()).days,
                    }

                chapters_data.append(data)
            
            # Include the course title in the response
            response = {
                'chapters': chapters_data,
                'course_title': course.title,
            }

            return Response(response, status=status.HTTP_200_OK)
        
        # If course does not exist or belongs to another user
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    bad_response = {
        'error': 'User not authenticated.',
    }
    # User not authenticated
    return Response(bad_response, status=status.HTTP_401_UNAUTHORIZED)


# Get flashcards for a chapter using the chapter id
@api_view(["POST"])
def getCards(request):
    # First confirm if user access token is valid
    user = request.user
    if user.is_authenticated:
        # Get the chapter id
        chapter_id = request.data.get('chapter_id')
        chapter = Chapter.objects.filter(id=chapter_id, course__owner=user).first()

        # Check if chapter exists
        if chapter:
            cards = Card.objects.filter(chapter=chapter).order_by('order')
            card_data = []
            for card in cards:
                card_data.append({
                    'id': card.id,
                    'question': card.question,
                    'answer': card.answer,
                    'order': card.order,
                })
            
            # Include the chapter title in the response
            response = {
                'cards': card_data,
                'chapter_title': chapter.chapter_title,
                'next_due': {},
                'last_revision': {},
            }

            # Check if the chapter has a next due date
            if chapter.next_due:
                response['next_due'] = {
                    'date': chapter.next_due.strftime('%Y-%m-%d'),
                    'days': (chapter.next_due - timezone.now()).days,
                }
                
            # Check if the chapter has a last revision
            score = { "mistakes": -1, "inputs": -1, "revised_today": False }
            chapter = Chapter.objects.get(id=chapter_id)
            last_revision = Revision.objects.filter(chapter=chapter).order_by('-date').first()
            if last_revision:
                score.update({
                    "mistakes": last_revision.mistakes,
                    "inputs": last_revision.inputs,
                })

                # Check if the chapter was revised today
                if last_revision.date.date() == datetime.now().date():
                    score.update({"revised_today": True})

            response['last_revision'] = score

            return Response(response, status=status.HTTP_200_OK)
        
        # If chapter does not exist
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # User not authenticated
    return Response(status=status.HTTP_401_UNAUTHORIZED)



# ------------------- Edit Requests -------------------

# Makes changes to a user's courses
@api_view(["POST"])
def changeCourses(request):
    # First confirm if user access token is valid
    user = request.user
    if user.is_authenticated:
        return editCourses(request, user)

    else:
        bad_response = {
            'error': 'User not authenticated.',
        }
        return Response(bad_response, status=status.HTTP_401_UNAUTHORIZED)
    

# Make changes to a user's chapters within a course
@api_view(["POST"])
def changeChapters(request):
    # First confirm if user access token is valid
    user = request.user
    if user.is_authenticated:
        return editChapters(request, user)

    else:
        bad_response = {
            'error': 'User not authenticated.',
        }
        return Response(bad_response, status=status.HTTP_401_UNAUTHORIZED) 


# Make changes to a user's flashcards within a chapter
@api_view(["POST"])
def changeCards(request):
    # First confirm if user access token is valid
    user = request.user
    if user.is_authenticated:
        return editCards(request, user)

    else:
        bad_response = {
            'error': 'User not authenticated.',
        }
        return Response(bad_response, status=status.HTTP_401_UNAUTHORIZED)
   


