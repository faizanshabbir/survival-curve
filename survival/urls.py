from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.home),
	url(r'^home$',views.home),
	url(r'^input_data$', views.input_data),
	url(r'^survey$', views.survey),
	url(r'^random_curve$', views.random_curve),
	url(r'^random_data$', views.random_data),
	url(r'^humza_input$', views.humza_input),
	url(r'^generate_curve$',views.generate_curve),
	url(r'^about$', views.about),
	url(r'^login$', 'django.contrib.auth.views.login'),
	url(r'^login_form$', views.user_login),
	url(r'^logout$', views.user_logout),
	url(r'^register$', views.register),
	url(r'^subscribe$', views.subscribe),
	url(r'^home_telephasic$',views.home_telephasic),
	url(r'^contact$',views.contact),
	url(r'^dev$', views.dev),
	url(r'^dev_about$', views.dev_about)
)