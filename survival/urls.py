from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.home),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)