from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="append")
@stringfilter
def append(value: str, arg: str):
    """Append a string to another string"""
    return value + arg


@register.filter(name="prepend")
@stringfilter
def prepend(value: str, arg: str):
    """Prepend a string to another string"""
    return arg + value
