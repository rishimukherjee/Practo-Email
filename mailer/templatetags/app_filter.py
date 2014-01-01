from django import template
import json

register = template.Library()

@register.filter(name='key')
def key(list_name, key_id):
    """
    Filter for getting value from an array
    Example
    -------
    Input: [hello, world, namaskar], 1
    Output: world
    """
    key_name = int(key_id)
    return list_name[key_id]

key = register.filter('key', key)


@register.filter(name='listify')
def listify(email_json):
    """
    
    Filter to clean a json array.
    Example
    ------- 
    Input: '["hello", "world", "how"]'
    Output: hello, world, how
    Note - '...' is added to the output if length of ouput >= than 35.

    """
    ret = email_json.strip()[1:-1].strip().replace("\"", "")[:35]
    if len(ret) >= 35: return ret + "..."
    return ret

listify = register.filter('listify', listify)