from urllib.parse import urlencode
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    #Urlencode makes a random order out of dicts, but preserves order of tuples. In order for tests to pass
    # the order must be fixed and thus the GET.dict() and kwargs must be converted to a list of tuples
    query = context['request'].GET.dict()
    new_query = []
    for key, value in query.items():
        dict_tuple = (key, value)
        new_query.append(dict_tuple)

    for key, value in kwargs.items():
        dict_tuple = (key, value)
        new_query.append(dict_tuple)
        
    return urlencode(new_query)
