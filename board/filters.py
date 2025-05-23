import django_filters
from .models import Ad


class AdFilter(django_filters.FilterSet):
    class Meta:
        model = Ad
        fields = {
            "category": ["exact"],
            "title": ["icontains"],
        }
