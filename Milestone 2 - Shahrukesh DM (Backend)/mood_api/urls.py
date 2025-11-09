from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PredictMoodView, UserViewSet, HistoryView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('predict-mood/', PredictMoodView.as_view(), name='predict-mood'),
    path('history/<int:user_id>/', HistoryView.as_view(), name='history'),
    path('', include(router.urls)),
]
