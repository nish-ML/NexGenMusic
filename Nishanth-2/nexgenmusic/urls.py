from django.contrib import admin
from django.urls import path, re_path
from api import views
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import redirect

schema_view = get_schema_view(
   openapi.Info(title="NexGenMusic API", default_version='v1'),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirect root / to frontend index.html
    path('', lambda request: redirect('/frontend/index.html', permanent=False)),

    path('api/register/', views.register),
    path('api/login/', views.login),
    path('api/refresh/', TokenRefreshView.as_view()),
    path('api/history/', views.history),
    path('api/generate/', views.generate_music),

    # Swagger / Redoc
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
