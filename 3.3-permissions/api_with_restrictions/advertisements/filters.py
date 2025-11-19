import django_filters
from django_filters import rest_framework as filters
from .models import Advertisement, AdvertisementStatusChoices

class AdvertisementFilter(filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()
    status = django_filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    
    class Meta:
        model = Advertisement
        fields = ['status', 'created_at', 'creator']