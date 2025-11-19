from django.contrib import admin 
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from advertisements.views import AdvertisementViewSet, FavoriteAdvertisementViewSet

router = DefaultRouter()
router.register('advertisements', AdvertisementViewSet, basename='advertisements')
router.register('favorites', FavoriteAdvertisementViewSet, basename='favorites')

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]