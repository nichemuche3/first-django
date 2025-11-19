from rest_framework import serializers
from .models import Advertisement, FavoriteAdvertisement, AdvertisementStatusChoices
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at']
        read_only_fields = ['creator', 'created_at', 'updated_at']

    def validate_status(self, value):
        """Валидация статуса"""
        if value not in AdvertisementStatusChoices.values:
            raise serializers.ValidationError("Недопустимый статус")
        return value

class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer(read_only=True)
    advertisement_id = serializers.PrimaryKeyRelatedField(
        queryset=Advertisement.objects.all(),
        source='advertisement',
        write_only=True
    )

    class Meta:
        model = FavoriteAdvertisement
        fields = ['id', 'user', 'advertisement', 'advertisement_id', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        """Валидация - нельзя добавить свое объявление в избранное"""
        user = self.context['request'].user
        advertisement = data['advertisement']
        
        if advertisement.creator == user:
            raise serializers.ValidationError("Нельзя добавить свое объявление в избранное")
        
        # Проверяем, не добавлено ли уже это объявление в избранное
        if FavoriteAdvertisement.objects.filter(user=user, advertisement=advertisement).exists():
            raise serializers.ValidationError("Это объявление уже в избранном")
        
        return data