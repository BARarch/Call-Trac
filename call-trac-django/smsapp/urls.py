from django.urls import re_path
from . import views


urlpatterns = [
	re_path(r'^$', views.app, name='twilio'),
	re_path(r'^send', views.send, name='send'),
	re_path(r'^sms', views.sms, name='sms')
]