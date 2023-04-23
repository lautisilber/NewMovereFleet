from django import template

register = template.Library()

# can be loaded usiing {% load index %}
@register.filter(name='dict_index')
def _filter_dict_index(dict_data, key):
    # usage example {{ your_dict|dict_index:your_key }}
    if key:
        return dict_data.get(key)