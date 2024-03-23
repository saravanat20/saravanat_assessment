# filters.py
import django_filters
from .models import Record

class RecordFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Record
        fields = ['name']
