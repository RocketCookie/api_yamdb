from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserCreateView,
                    UserReadViewSet, UserSendTokenView)

v1_router = DefaultRouter()
v1_router.register('users', UserReadViewSet)
v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('signup/', UserCreateView.as_view()),
    path('token/', UserSendTokenView.as_view()),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_urls)),
]
