from django import template

register = template.Library()

# can be loaded usiing {% load index %}
@register.filter(name='dict_index')
def _filter_dict_index(dict_data, key):
    # usage example {{ your_dict|dict_index:your_key }}
    if key:
        return dict_data.get(key)

@register.filter(name='list_index')
def _filter_list_index(indexable, i):
    # usage example {{ your_list|list_index:index }}
    return indexable[i]

@register.filter(name='get_attr')
def _filter_list_index(obj, attr):
    # usage example {{ your_obj|get_attr:attr }}
    if hasattr(obj, attr):
        return getattr(obj, attr)