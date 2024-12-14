from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from books.views import auth, UserBookRelationView

router = SimpleRouter()
router.register(r'book_relation', UserBookRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('books.urls', namespace='books')),
    path('users/', include('users.urls', namespace='users')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('social_django.urls', namespace='social')),
    path('api/v1/auth/', auth, name='auth'),
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns+=router.urls