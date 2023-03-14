from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet

v1_router = routers.DefaultRouter()
v1_router.register('titles', TitleViewSet)
# v1_router.register('follow', FollowViewSet, basename='follow')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
