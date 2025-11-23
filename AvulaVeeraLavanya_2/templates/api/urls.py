from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, GenerateView, HistoryView


urlpatterns = [
	path("register/", RegisterView.as_view(), name="register"),
	path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
	path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
	path("generate/", GenerateView.as_view(), name="generate"),
	path("history/", HistoryView.as_view(), name="history"),
]


