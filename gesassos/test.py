from django.contrib.auth.models import User

def callbackfunction(tree):
    username = tree[0][0].text
    user_login, user_created = User.objects.get_or_create(username=username)
    # profile, created = user.profile
    # print(profile)
    # profile.email = tree[0][1].text
    # profile.position = tree[0][2].text
    # profile.save()