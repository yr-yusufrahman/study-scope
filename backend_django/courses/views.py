from django.shortcuts import render

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Course


@api_view(["GET"])
def all_courses(request):
    # First confirm if user access token is valid
    user = request.user
    if user:
        courses = Course.objects.filter(owner=user)
        courses_data = []
        for course in courses:
            courses_data.append({
                'id': course.id,
                'title': course.title,
            })
        response = {
            'courses': courses_data,
        }

        return Response(response, status=status.HTTP_200_OK)
    
    bad_response = {
        'error': 'User not authenticated.',
    }
    return Response(bad_response, status=status.HTTP_401_UNAUTHORIZED)