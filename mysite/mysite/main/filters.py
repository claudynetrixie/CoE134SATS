import django_filters
from .models import *


class StudentFilter(django_filters.FilterSet):
    STATUS = (
        ('GR1', 'GR1'),
        ('GR2', 'GR2'),
        ('GR3', 'GR3'),
    )
    name = django_filters.CharFilter(lookup_expr='iexact')
    # year_level = django_filters.ChoiceFilter(choices= STATUS)

    class Meta:
        model = Student
        fields = '__all__'
        fields = ['first_name', 'year_level']