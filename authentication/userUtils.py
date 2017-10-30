from django.contrib.auth.models import Group

def has_group(user, group_name):
    if user.is_superuser:
        return True

    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all()

def has_group_in(user, group_names):
    # Same as above but we want the user to be in at least
    # one of the given groups.
    group_names = group_names.split(",")
    for group in group_names:
        if has_group(user, group):
            return True
    return False