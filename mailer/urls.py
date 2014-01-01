from django.conf.urls import patterns, url

from mailer import views

urlpatterns = patterns('',
    url(r'^$', views.patients, name='patients'),
    url(r'^$', views.mail, name='email'),
)
