from django.conf.urls import url

from . import views

app_name = 'gesmail'
urlpatterns = [
    # ex: /gesmail/
    url(r'^$', views.index, name='index'),
    # ex: /gesmail/all/
    url(r'^(?P<all>\w+)/$', views.detail, name='detail'),
]