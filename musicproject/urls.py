from django.contrib import admin
from django.urls import path, include, re_path
from music_app.views import home, history_api, register_api, login_api, register_view, login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Music Generator API",
        default_version='v1',
        description="API for music generation with sentiment analysis",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@musicgen.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/history/', history_api, name='history_api'),
    path('api/register/', register_api, name='register_api'),
    path('api/login/', login_api, name='login_api'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
