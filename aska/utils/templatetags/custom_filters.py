from django import template

from utils.helpers.time_manipulation import get_relative_time

register = template.Library()


@register.filter(name="relative_time")
def relative_time(datetime):
    return get_relative_time(datetime)
