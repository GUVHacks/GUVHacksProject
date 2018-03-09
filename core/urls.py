from django.conf.urls import url
from django.contrib import admin
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^account-setup/$', views.account_setup, name='account-setup'),
    url(r'^history/$', views.history, name='history'),
]
