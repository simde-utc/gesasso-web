from django import template
from django.contrib.auth.models import Group 

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    if user.is_superuser:
        return True

    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all()

@register.filter(name='has_group_in') 
def has_group_in(user, group_names):
    # Same as above but we want th user to be in at least
    # one of the given groups.
    group_names = group_names.split(",")
    for group in group_names:
        if has_group(user, group):
            return True
    return False