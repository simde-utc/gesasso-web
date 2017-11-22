from django.conf.urls import url, include
import cas.views

from . import views

# API endpoints
app_name = 'authentication'
urlpatterns = [
    url(r'^login/$', cas.views.login, name='login'),
    url(r'^logout/$', cas.views.logout, name='logout'),
]
