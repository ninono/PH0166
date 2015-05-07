# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    k=key
    if type(key)==long:
        k=str(key)
    return dictionary[k]
