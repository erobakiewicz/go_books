from rest_framework.routers import DefaultRouter

from books.views import BookViewSet

app_name = "books_api"

router = DefaultRouter()
router.register(r'books_api', BookViewSet.as_view(), basename="books_api")

urlpatterns = router.urls
