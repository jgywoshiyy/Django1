# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [

    url('^login/$', views.login),
    url('^login_handle/$', views.login_handle),

    url('^register/$', views.register),
    url('^register_valid/$', views.register_valid),
    url('^register_valid1/$', views.register_valid1),

    url('^register_handle/$', views.register_handle),
    url('^verify_code/$', views.verify_code),
]
