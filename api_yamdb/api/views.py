# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework import filters
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import AuthorOrSuperUserOrAdminOrReadOnly
from .serializers import (CommentSerializer, UserCreateSerializer,
                          ReviewSerializer, TitleSerializer)
from .utilities import send_confirm_code
from reviews.models import Review, Title, User


class UserCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = request.data.get('email')
            username = request.data.get('username')
            user = User.objects.get(username=username)
            confirm_code = default_token_generator.make_token(user)
            send_confirm_code(email, confirm_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    # pagination_class = LimitOffsetPagination

    # def get_title(self):
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
    # pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
