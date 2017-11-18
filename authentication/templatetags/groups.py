from django import template
from authentication import userUtils

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return userUtils.has_group(user, group_name)

@register.filter(name='has_group_in') 
def has_group_in(user, group_names):
    return userUtils.has_group_in(user, group_names)