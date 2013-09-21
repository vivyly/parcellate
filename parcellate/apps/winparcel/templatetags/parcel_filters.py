from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def http_prepend(value):
    if value.startswith('http://'):
        return value
    else:
        return 'http://%s' % value
