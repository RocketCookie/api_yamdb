from rest_framework import viewsets
from reviews.models import Title
from .serializers import TitleSerializer
# from rest_framework.permissions import (IsAdminUser)
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework import filters


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет POST, GET, PATCH, DELETE методы для Title сериализатора"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (IsAdminUser)
    # pagination_class = LimitOffsetPagination
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('category__slug', 'genre__slug', 'year')