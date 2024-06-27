from django.shortcuts import render

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime

from ..models import Course, Chapter, Card


def editCourses(request, user):
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
            new_course = Course.objects.filter(owner=user, title=course_title).first()
            if not new_course:
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
    

def editChapters(request, user):
    additions = request.data.get('add')
    edits = request.data.get('edit')
    removals = request.data.get('remove')
    moves = request.data.get('move')
    switches = request.data.get('switch')
    new_course_id = switches.get('new_course_id')
    switch_id = switches.get('id')

    course_id = request.data.get('course_id')
    course = Course.objects.filter(owner=user, id=course_id).first()
    confirmed_order = [] # List of chapter ids that have already been placed in correct order
    new_course = Course.objects.filter(owner=user, id=new_course_id).first()

    # Remove chapters
    if removals:
        for removal in removals:
            chapter_id = removal.get('id')
            chapter = Chapter.objects.filter(course=course, id=chapter_id).first()
            if chapter:
                chapter.delete()

    # Add new chapters
    if additions:
        for addition in additions:
            temp_id = addition.get('id')
            chapter_title = addition.get('title')

            # a newly created chapter may be switched to another course
            if temp_id in switch_id:
                chapter = Chapter.objects.create(course=new_course, chapter_title=chapter_title)
                chapter.switchCourse()
                chapter.save()
            else:
                chapter_order = moves.index(temp_id)
                chapter = Chapter.objects.create(course=course, chapter_title=chapter_title, order=chapter_order)
                chapter.save()
                confirmed_order.append(temp_id)
    
    # Edit existing chapters
    if edits:
        for edit in edits:
            chapter_id = edit.get('id')
            chapter_title = edit.get('new_title')

            chapter = Chapter.objects.filter(course=course, id=chapter_id).first()
            if chapter:
                # Check if the title was changed
                if chapter_title != chapter.chapter_title:
                    chapter.chapter_title = chapter_title

                    # An edited chapter may be switched to another course
                    if chapter_id in switch_id:
                        chapter.course = new_course
                        chapter.switchCourse()
                        chapter.save()
                    else:
                        if moves:
                            chapter_order = moves.index(chapter_id) # Get the index of the chapter id in the move list
                            chapter.order = chapter_order
                            confirmed_order.append(chapter_id)
                        chapter.save()

    # Update the order of unmodified chapters
    if moves:
        for id in moves:
            if id not in confirmed_order:
                chapter = Chapter.objects.filter(course=course, id=id).first()
                chapter.order = moves.index(id)
                chapter.save()
                confirmed_order.append(id)

    # Switch the course of unmodified chapters
    if switch_id:
        for id in switch_id:
            chapter = Chapter.objects.filter(course=course, id=id).first()
            if chapter:
                chapter.course = new_course
                chapter.switchCourse()
                chapter.save()

    return Response(status=status.HTTP_200_OK)


def editCards(request, user):
    additions = request.data.get('add')
    edits = request.data.get('edit')
    removals = request.data.get('remove')
    moves = request.data.get('move')

    chapter_id = request.data.get('chapter_id')
    chapter = Chapter.objects.filter(id=chapter_id).first()
    confirmed_order = [] # List of card ids that have already been placed in correct order

    # Remove cards
    if removals:
        for removal in removals:
            card_id = removal.get('id')
            card = Card.objects.filter(chapter=chapter, id=card_id).first()
            if card:
                card.delete()


    # Add new cards
    if additions:
        for addition in additions:
            temp_id = addition.get('id')
            card_question = addition.get('question')
            card_answer = addition.get('answer')
            card_order = moves.index(temp_id) # Get the index of the card id in the move list
            
            card = Card.objects.create(question=card_question, answer=card_answer, order=card_order, chapter=chapter)
            card.save()
            confirmed_order.append(temp_id)
    
    # Edit existing cards
    if edits:
        for edit in edits:
            card_id = edit.get('id')
            card_question = edit.get('new_question')
            card_answer = edit.get('new_answer')

            card = Card.objects.filter(chapter=chapter, id=card_id).first()
            if card:
                card.question = card_question
                card.answer = card_answer
                if moves:
                    card_order = moves.index(card_id) # Get the index of the card id in the move list
                    card.order = card_order
                    confirmed_order.append(card_id)
                card.save()
    
    # Update the order of unchanged cards
    if moves:
        for move in moves:
            if move not in confirmed_order:
                card = Card.objects.filter(chapter=chapter, id=move).first()
                card.order = moves.index(move)
                card.save()
                confirmed_order.append(move)
    
    return Response(status=status.HTTP_200_OK)

   
