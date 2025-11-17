from rest_framework.routers import DefaultRouter
from .views import LivreViewSet

router = DefaultRouter()
router.register(r'livres', LivreViewSet, basename='livre')

urlpatterns = router.urls
