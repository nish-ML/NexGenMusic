from django.urls import path,include
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'music_records', views.MusicRecordViewSet)

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),   # default page
    path('index/', views.index_view, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path ('generate_music/', views.generate_music, name='generate_music'),
    path('api/', include(router.urls)),
]
