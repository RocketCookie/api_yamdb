from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (AdminOnly, AdminOrReadOnly,
                          AuthorOrModeratorOrAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserCreateSerializer, UserReadSerializer,
                          UserSendTokenSerializer)
from .utilities import send_confirm_code
from reviews.models import Category, Genre, Review, Title, User


class UserCreateView(APIView):
    """APIView создание пользователя"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user, _ = User.objects.get_or_create(
                **serializer.validated_data)
            confirm_code = default_token_generator.make_token(user)
            send_confirm_code(user.email, confirm_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSendTokenView(APIView):
    """APIView POST методы для получение токена"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSendTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')
            if not default_token_generator.check_token(user,
                                                       confirmation_code):
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReadViewSet(viewsets.ModelViewSet):
    """ViewSet GET, POST, PATCH, DELETE  методы для профиля пользователя"""
    queryset = User.objects.all().order_by('id')
    serializer_class = UserReadSerializer
    permission_classes = (AdminOnly,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['get', 'patch'],
            detail=False,
            url_path='me',
            permission_classes=[IsAuthenticated],)
    def me(self, request):
        if request.method == 'GET':
            serializer = UserReadSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserReadSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet POST, GET, DELETE методы для Genre сериализатора"""
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet POST, GET, DELETE методы для Category сериализатора"""
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для Title сериализатора"""
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для Review сериализатора"""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для Comment сериализатора"""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review())
