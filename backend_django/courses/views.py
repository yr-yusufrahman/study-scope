from django.shortcuts import render

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Course, Chapter, Card

# Returns all course data and chapter for a user
@api_view(["GET"])
def getCourses(request):
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
def changeCourses(request):
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
    

# Returns all chapters for a course
@api_view(["POST"])
def getChapters(request):
    # First confirm if user access token is valid
    user = request.user
    if user:
        course_id = request.data.get('course_id')
        course = Course.objects.filter(owner=user, id=course_id).first()

        # Check if course exists and belongs to user
        if course:
            # Get all chapters for the course
            chapters = Chapter.objects.filter(course=course)
            chapters_data = []

            for chapter in chapters:
                chapters_data.append({
                    'id': chapter.id,
                    'title': chapter.chapter_title,
                })
            
            response = {
                'chapters': chapters_data,
            }

            return Response(response, status=status.HTTP_200_OK)
        
        # If course does not exist or belongs to another user
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    bad_response = {
        'error': 'User not authenticated.',
    }
    return Response(bad_response, status=status.HTTP_401_UNAUTHORIZED)


# Make changes to a user's chapters within a course



# Get flashcards for a chapter using the chapter id
@api_view(["POST"])
def getCards(request):
    # First confirm if user access token is valid
    user = request.user
    if user:
        # Get the chapter id
        chapter_id = request.data.get('chapter_id')
        cards = Card.objects.filter(chapter=chapter_id).order_by('order')
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


# Make changes to a user's flashcards within a chapter
@api_view(["POST"])
def changeCards(request):
    # First confirm if user access token is valid
    user = request.user
    if user:
        additions = request.data.get('add')
        edits = request.data.get('edit')
        removals = request.data.get('remove')
        moves = request.data.get('move')

        chapter_id = request.data.get('chapter_id')
        chapter = Chapter.objects.filter(id=chapter_id).first()
        confirmed_order = [] # List of card ids that have already been placed in correct order

        # Remove courses
        if removals:
            for removal in removals:
                card_id = removal.get('id')
                card = Card.objects.filter(chapter=chapter, id=card_id).first()
                if card:
                    card.delete()


        # Add new courses
        if additions:
            for addition in additions:
                temp_id = addition.get('id')
                card_question = addition.get('question')
                card_answer = addition.get('answer')
                card_order = moves.index(temp_id) # Get the index of the card id in the move list
                
                card = Card.objects.create(question=card_question, answer=card_answer, order=card_order, chapter=chapter)
                card.save()
                confirmed_order.append(temp_id)
        
        # Edit existing courses
        if edits:
            for edit in edits:
                card_id = edit.get('id')
                card_question = edit.get('question')
                card_answer = edit.get('answer')
                card_order = moves.index(card_id) # Get the index of the card id in the move list

                card = Card.objects.filter(chapter=chapter, id=card_id).first()
                if card:
                    card.question = card_question
                    card.answer = card_answer
                    card.order = card_order
                    card.save()
                    confirmed_order.append(card_id)
        
        # Update the order of unchanged cards
        if moves:
            for move in moves:
                if move not in confirmed_order:
                    card = Card.objects.filter(chapter=chapter, id=move).first()
                    card.order = moves.index(move)
                    card.save()
                    confirmed_order.append(move)
        
        return Response(status=status.HTTP_200_OK)

    else:
        bad_response = {
            'error': 'User not authenticated.',
        }
        return Response(bad_response, status=status.HTTP_401_UNAUTHORIZED)
   


