from django.urls import path, include
from .views import googleLogin, googleAuth, refreshAuth, devBypassLogin

from .views import home, logout_google


urlpatterns = [    
    # This is for the frontend to go to google sign-in page
    path('login/google', view=googleLogin, name='google_login'),
    path('auth/google', view=googleAuth, name='google_auth'),
    path('auth/refresh', view=refreshAuth, name='refresh_auth'),
    path('auth/dev-login', view=devBypassLogin, name='dev_bypass_login'),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),

    path("", home),
    path("logout", logout_google),
]

