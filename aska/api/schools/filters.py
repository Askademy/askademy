from django_filters import rest_framework as filters

from records.schools.models import School

class SchoolFilter(filters.FilterSet):
    class Meta:
        model = School
        fields = ["name", "owner", "district"]