from datetime import timedelta

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils import timezone

from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import requests


# Gets auth code from google after user logs in
@api_view(["GET"])
def googleLogin(request):
    CLIENT_ID = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
    NEXT = "http://localhost:5173/login"
    redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email&access_type=offline&redirect_uri={NEXT}"
    return redirect(redirect_url)


# Exchanges auth code for google token and then exchanges google token for local token
@api_view(["POST"])
def googleAuth(request):
    code = request.data['code']
    if code:
        # Prepare the request parameters to exchange the auth code for access token
        CLIENT_ID = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        CLIENT_SECRET = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
        NEXT = "http://localhost:5173/login"

        token_endpoint = 'https://oauth2.googleapis.com/token'
        token_params = {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': NEXT,
            'grant_type': 'authorization_code'
        }
        response = requests.post(token_endpoint, data=token_params)
   
        if response.ok:
            google_token = response.json().get('access_token')
        
            if google_token:
                # Get user's profile data
                profile_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'    
                headers = {'Authorization': f'Bearer {google_token}'}
                profile_response = requests.get(profile_endpoint, headers=headers)
                
                if profile_response.ok:
                    data = {}
                    profile_data = profile_response.json()
                    
                    # Create user if needed - This may not be needed, library does this for you, check with new user login
                    email = profile_data["email"]
                    name = profile_data["given_name"]

                    # Use google token to create local token
                    exchange_endpoint = 'http://127.0.0.1:8000/auth/convert-token'
                    exchange_params = {
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET,
                        'grant_type': 'convert_token',
                        'backend': 'google-oauth2',
                        'token': google_token
                    }

                    server_response = requests.post(exchange_endpoint, data=exchange_params)
                    if server_response.ok:
                        access_token = server_response.json().get('access_token')
                        refresh_token = server_response.json().get('refresh_token')
                        data['access_token'] = access_token
                        data['refresh_token'] = refresh_token
                        data['email'] = email
                        data['name'] = name

                        return Response(data, status.HTTP_201_CREATED)

    return Response({}, status.HTTP_400_BAD_REQUEST)
# EMD googleAuth


# Use refresh token to gain new local access token
@api_view(["POST"])
def refreshAuth(request):
    refresh_token = request.data['refresh']
    if refresh_token:
        CLIENT_ID = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        CLIENT_SECRET = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

        refresh_endpoint = 'http://127.0.0.1:8000/auth/token'
        refresh_params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        server_response = requests.post(refresh_endpoint, data=refresh_params)
        if server_response.ok:
            access_token = server_response.json().get('access_token')
            refresh_token = server_response.json().get('refresh_token')
            data = {}
            data['access_token'] = access_token
            data['refresh_token'] = refresh_token

            return Response(data, status.HTTP_201_CREATED)
        
    return Response({}, status.HTTP_400_BAD_REQUEST)

# END refreshAuth


def _dev_login_user():
    return (
        User.objects.annotate(course_count=Count("course"))
        .filter(course_count__gt=0)
        .order_by("-course_count", "id")
        .first()
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def devBypassLogin(request):
    remote = request.META.get("REMOTE_ADDR")
    if not settings.DEBUG or remote not in ("127.0.0.1", "::1"):
        return Response({"detail": "Not available."}, status=status.HTTP_403_FORBIDDEN)

    user = _dev_login_user()
    if not user:
        return Response({"detail": "No user with courses found."}, status=status.HTTP_404_NOT_FOUND)

    application = Application.objects.first()
    if not application:
        return Response({"detail": "OAuth application not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token = AccessToken.objects.create(
        user=user,
        application=application,
        token=generate_token(),
        expires=expires,
        scope="read write",
    )
    refresh_token = RefreshToken.objects.create(
        user=user,
        application=application,
        token=generate_token(),
        access_token=access_token,
    )

    name = user.first_name or user.username
    if user.last_name:
        name = f"{user.first_name} {user.last_name}".strip() or name

    return Response(
        {
            "access_token": access_token.token,
            "refresh_token": refresh_token.token,
            "email": user.email,
            "name": name,
        },
        status=status.HTTP_201_CREATED,
    )


# Create your views here.
def home(request):
    name = ""
    return render(request, 'google.html', {'first_name': name})


def logout_google(request):
    logout(request)
    return redirect('http://localhost:5173')





