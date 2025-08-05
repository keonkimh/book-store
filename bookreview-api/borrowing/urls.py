from django.urls import path
from .views import BorrowViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'', BorrowViewSet, basename='borrow')

urlpatterns = router.urls