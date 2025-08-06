from rest_framework.routers import SimpleRouter

from .views import BorrowViewSet

router = SimpleRouter()
router.register(r"", BorrowViewSet, basename="borrow")

urlpatterns = router.urls
