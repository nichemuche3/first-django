from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Advertisement, FavoriteAdvertisement
from .serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsOwnerOrAdmin

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий"""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action in ["favorite", "favorites"]:
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

    def get_queryset(self):
        """Фильтрация объявлений для разных пользователей"""
        queryset = super().get_queryset()
        
        if not self.request.user.is_authenticated:
            queryset = queryset.exclude(status="DRAFT")
        elif not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(status__in=["OPEN", "CLOSED"]) | 
                Q(creator=self.request.user)
            )
        
        return queryset

    def perform_create(self, serializer):
        """Автоматическое назначение создателя объявления"""
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """Добавить объявление в избранное"""
        advertisement = self.get_object()
        
        if advertisement.creator == request.user:
            return Response(
                {"error": "Нельзя добавить свое объявление в избранное"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if FavoriteAdvertisement.objects.filter(
            user=request.user, 
            advertisement=advertisement
        ).exists():
            return Response(
                {"error": "Объявление уже в избранном"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        favorite = FavoriteAdvertisement.objects.create(
            user=request.user,
            advertisement=advertisement
        )
        
        serializer = FavoriteAdvertisementSerializer(
            favorite, 
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def favorites(self, request):
        """Получить избранные объявления пользователя"""
        favorites = FavoriteAdvertisement.objects.filter(user=request.user)
        page = self.paginate_queryset(favorites)
        
        if page is not None:
            serializer = FavoriteAdvertisementSerializer(
                page, 
                many=True, 
                context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        
        serializer = FavoriteAdvertisementSerializer(
            favorites, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)

class FavoriteAdvertisementViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteAdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteAdvertisement.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)