from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('generate-music/', views.MusicGenerationAPIView.as_view(), name='generate-music'),
    path('history/', views.UserHistoryAPIView.as_view(), name='history'),
]
