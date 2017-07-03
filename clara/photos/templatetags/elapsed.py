from django import template
from django.utils import timezone
register = template.Library()


@register.filter(expects_localtime=True)
def elapsed(time, seconds):
    return time + timezone.timedelta(seconds=seconds) < timezone.now()
