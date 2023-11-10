from django_filters import rest_framework as filters
from django.db.models import Q

from users.models import CustomUser

class CustomUserFilter(filters.FilterSet):
    phone_number = filters.CharFilter(lookup_expr='icontains')
    username = filters.CharFilter(method='filter_username',label="username")

    def filter_username(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(middle_name__icontains=value) | Q(last_name__icontains=value)
        )

    class Meta:
        model = CustomUser
        fields = ["phone_number", "username", "gender", "level"]