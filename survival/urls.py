from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.home),
	url(r'^home$',views.home),
	url(r'^curve$', views.curve),
	url(r'^survey$', views.survey),
	url(r'^random_data$', views.random_data),
	url(r'^generate_curve$',views.generate_curve),
	url(r'^about$', views.about),
	url(r'^contact$',views.contact),
	url(r'^sign_up$',views.sign_up),
	url(r'^login$', 'django.contrib.auth.views.login'),
	url(r'^login_form$', views.user_login),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^register$', views.register),
	url(r'^contactKM$',views.contactKM),
	url(r'^subscribe$', views.subscribe),
	url(r'^email-signup$',views.email_signup),
)