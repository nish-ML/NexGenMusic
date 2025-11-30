from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from api import views
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(title="NexGenMusic API", default_version='v1'),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/register/', views.register),
    path('api/login/', views.login),
    path('api/refresh/', TokenRefreshView.as_view()),
    path('api/google-auth/', views.google_auth),
    path('api/google-callback/', views.google_callback),
    path('api/generate/', views.generate_music),
    path('api/generate-playlist/', views.generate_playlist),
    path('api/analyze-sentiment/', views.analyze_sentiment),
    path('api/history/', views.history),
    path('api/generate-audio/', views.generate_audio),
    path('api/generate-midi/', views.generate_midi_music),
    path('api/audio/<str:filename>', views.serve_audio),
    path('api/music/<str:filename>', views.serve_music),
    
    # User Profile & Library endpoints
    path('api/profile/', views.user_profile),
    path('api/playlists/', views.playlists),
    path('api/playlists/<int:pk>/', views.playlist_detail),
    path('api/playlists/<int:pk>/add/', views.add_to_playlist),
    path('api/favorites/', views.favorites),
    path('api/favorites/<int:pk>/', views.favorite_detail),
    path('api/downloads/', views.downloads),
    path('api/downloads/<int:pk>/', views.download_detail),

    # Swagger UI
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Serve frontend templates - Premium 3D as default
    path('', TemplateView.as_view(template_name="premium-3d-login.html"), name='home'),
    path('premium-login/', TemplateView.as_view(template_name="premium-3d-login.html"), name='premium_login'),
    path('premium-register/', TemplateView.as_view(template_name="premium-3d-register.html"), name='premium_register'),
    
    # Original neon pages (still accessible)
    path('neon-login.html', TemplateView.as_view(template_name="neon-login.html"), name='neon_login'),
    path('neon-register.html', TemplateView.as_view(template_name="neon-register.html"), name='neon_register'),
    
    path('dashboard/', TemplateView.as_view(template_name="dashboard_premium.html"), name='dashboard'),
    path('game/', TemplateView.as_view(template_name="game-with-layout.html"), name='game'),
    path('game-test/', TemplateView.as_view(template_name="game-test-simple.html"), name='game_test'),
    path('ai-generator/', TemplateView.as_view(template_name="premium_ai_generator.html"), name='ai_generator'),
    path('spotify-recommendations/', TemplateView.as_view(template_name="spotify_green.html"), name='spotify_recommendations'),
    path('history/', TemplateView.as_view(template_name="history_green.html"), name='history'),
    path('about/', TemplateView.as_view(template_name="about_green.html"), name='about'),
    
    # Library pages - using green theme templates
    path('library/', TemplateView.as_view(template_name="library_premium.html"), name='library'),
    path('library/favorites/', TemplateView.as_view(template_name="favorites_green.html"), name='library_favorites'),
    path('library/playlists/', TemplateView.as_view(template_name="playlists_premium.html"), name='library_playlists'),
    
    # User profile pages
    path('profile/', TemplateView.as_view(template_name="profile_green.html"), name='profile'),
    path('settings/', TemplateView.as_view(template_name="settings_green.html"), name='settings'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
