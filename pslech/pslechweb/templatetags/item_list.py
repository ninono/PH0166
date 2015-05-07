from django.template import Library
register=Library()
@register.filter
def item_list(obj):
    return [obj]
