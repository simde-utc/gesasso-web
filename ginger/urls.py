from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'ginger'
urlpatterns = [
    url(r'^contributors$', views.contributors, name='contributors'),
    url(r'^api$', views.api, name='api_keys'),
]