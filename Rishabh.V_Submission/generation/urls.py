from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GenerateMusicViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'music', GenerateMusicViewSet, basename='music')

urlpatterns = router.urls
