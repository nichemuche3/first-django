from rest_framework import permissions
from .models import AdvertisementStatusChoices

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение на изменение/удаление только для владельца объявления.
    """
    def has_object_permission(self, request, view, obj):
        # Чтение разрешено для всех запросов
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Запись разрешена только владельцу
        return obj.creator == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение на изменение/удаление для администраторов.
    """
    def has_permission(self, request, view):
        # Чтение разрешено для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Запись разрешена только администраторам
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Запись разрешена только администраторам
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешение на просмотр/изменение только для владельца или администратора.
    """
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or (request.user and request.user.is_staff)