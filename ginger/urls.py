from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from authentication import decorator as auth

from . import views

app_name = 'ginger'
urlpatterns = [
    url(r'^contributors$',  auth.group_required("bde", "simde")(views.contributors), name='contributors'),
    url(r'^api$', auth.group_required("bde", "simde", "bureau", "geek")(views.api), name='api'),
    url(r'^api/(?P<key>\w*)/delete$', auth.group_required("simde")(views.delete_key), name='delete_key'),
    url(r'^api/(?P<key>\w*)/renew$', auth.group_required("simde", "bureau", "geek")(views.renew_key), name='renew_key'),
    url(r'^infos$', views.info, name='info_self'),
    url(r'^infos/(?P<login>\w*)$', auth.group_required("bde", "simde")(views.info), name='info'),
]