
from rest_framework import viewsets
from reviews.models import Title, Review
from .serializers import TitleSerializer, CommentSerializer, ReviewSerializer
# from rest_framework.permissions import (IsAdminUser)
from .permissions import AuthorOrSuperUserOrAdminOrReadOnly
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework import filters
from django.shortcuts import get_object_or_404


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет POST, GET, PATCH, DELETE методы для Title сериализатора"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (IsAdminUser)
    # pagination_class = LimitOffsetPagination
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('category__slug', 'genre__slug', 'year')

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrSuperUserOrAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    #def get_title(self):
    #    return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrSuperUserOrAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )

