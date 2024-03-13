from django.urls import path, include
from .views import home, logout_google

from .views import googleLogin, googleAuth


urlpatterns = [
    path("", home),
    
    # This is for the frontend to go to google sign-in page
    path('login/google', view=googleLogin, name='google_login'),
    path('auth/google', view=googleAuth, name='google_auth'),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),

    path("logout", logout_google),
]

