from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from authentication import decorator as auth

from . import views

app_name = 'ginger'
urlpatterns = [
    url(r'^contributors$',  auth.group_required("bde", "simde")(views.contributors), name='contributors'),
    url(r'^api$', auth.group_required("bde", "simde", "bureau", "geek")(views.api), name='api_keys'),
]