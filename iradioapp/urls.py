from django.conf.urls import patterns, include, url
from iradioapp import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^command/$', views.command, name='command'),
)
