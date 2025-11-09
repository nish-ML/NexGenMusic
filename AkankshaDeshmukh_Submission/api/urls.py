# spotify_app/urls.py

from django.urls import path
from .views import (
    login_page,
    register_page,
    dashboard,
    api_register,
    api_login,
    GenerateMusicAPI,
    music_history,  # Added for history API
)

urlpatterns = [
    # Pages
    path("", login_page),
    path("login/", login_page),
    path("register/", register_page),
    path("dashboard/", dashboard),

    # API endpoints
    path("api/register/", api_register),
    path("api/login/", api_login),
    path("api/genmusic/", GenerateMusicAPI.as_view()),
    path("api/history/", music_history, name="music_history"),  # History API
]
