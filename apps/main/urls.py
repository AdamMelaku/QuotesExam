from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_user$', views.register),
    url(r'^login_user$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$',views.dashboard),
    url(r'^users/(?P<id>\d+)/$', views.user_info),
    url(r'^favorites/(?P<id>\d+)/$', views.favorites),
    url(r'^remove/(?P<id>\d+)/$', views.remove),
    url(r'^add_quote$',views.add_quote),
]
