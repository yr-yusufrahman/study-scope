from django.shortcuts import render

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Course, Chapter, Card

# Returns all course data for a user
@api_view(["GET"])
def all_courses(request):
    # First confirm if user access token is valid
    user = request.user
    if user:
        # All courses for the user
        courses = Course.objects.filter(owner=user)
        courses_data = []
        for course in courses:
            # All chapters for the course
            chapters = Chapter.objects.filter(course=course)
            courses_data.append({
                'id': course.id,
                'title': course.title,
                'chapters': [{
                    'id': chapter.id,
                    'title': chapter.chapter_title,
                } for chapter in chapters],
            })
            
        response = {
            'courses': courses_data,
        }

        return Response(response, status=status.HTTP_200_OK)
    
    bad_response = {
        'error': 'User not authenticated.',
    }
    return Response(bad_response, status=status.HTTP_401_UNAUTHORIZED)


# Makes changes to a user's courses
@api_view(["POST"])
def change_courses(request):
    # First confirm if user access token is valid
    user = request.user
    if user:
        additions = request.data.get('add')
        edits = request.data.get('edit')
        removals = request.data.get('remove')

        # Remove courses
        if removals:
            for removal in removals:
                course_id = removal.get('id')
                course = Course.objects.filter(owner=user, id=course_id).first()
                if course:
                    course.delete()

        # Add new courses
        if additions:
            for addition in additions:
                course_title = addition.get('title')
                course = Course.objects.create(owner=user, title=course_title)
                course.save()
        
        # Edit existing courses
        if edits:
            for edit in edits:
                course_id = edit.get('id')
                course_title = edit.get('new_title')
                course = Course.objects.filter(owner=user, id=course_id).first()
                if course:
                    # Check if the title was changed
                    if course_title != course.title:
                        course.title = course_title
                        course.save()
        
        return Response(status=status.HTTP_200_OK)

    else:
        bad_response = {
            'error': 'User not authenticated.',
        }
        return Response(bad_response, status=status.HTTP_401_UNAUTHORIZED)
    

# Make changes to a user's chapters within a course
    


# Get flashcards for a chapter using the chapter id
@api_view(["POST"])
def get_cards(request):
    # First confirm if user access token is valid
    user = request.user
    if user:
        # Get the chapter id
        chapter_id = request.data.get('chapter_id')
        cards = Card.objects.filter(chapter=chapter_id)
        card_data = []
        for card in cards:
            card_data.append({
                'id': card.id,
                'question': card.question,
                'answer': card.answer,
                'order': card.order,
            })
        
        response = {
            'cards': card_data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_401_UNAUTHORIZED)