from django.conf.urls import patterns, include, url

from mailer import views

urlpatterns = patterns('',
    url(r'^$', views.homepage),
    url(r'^patients/', views.patients),
    url(r'^email/', views.mail),
    url(r'^sent/', views.sentmail),
)
