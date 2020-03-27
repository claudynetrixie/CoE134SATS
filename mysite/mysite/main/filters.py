import django_filters
from .models import *


class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        #fields = ['first_name', 'year_level', 'section']
        fields = ['year_level']


class LogFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Log
        fields = ['date']