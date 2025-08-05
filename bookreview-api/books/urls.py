from django.urls import path
from .views import BookViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'', BookViewSet, basename='book')

urlpatterns = router.urls