from django.urls import path
from . import views

urlpatterns = [
    # Home & Authentication
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Upload image
    path('upload/', views.upload_image, name='upload_image'),

    # Music generation (handles mood, sentiment, Spotify tracks, and generated music)
    path('music/', views.music_generation_view, name='music_generation'),

    # If you have a separate mood detection view, uncomment this and make sure it exists in views.py
    # path('mood/', views.mood_detection_view, name='mood_detection'),
]
