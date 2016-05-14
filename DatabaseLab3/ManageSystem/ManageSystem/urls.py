"""ManageSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mysite.views import *

urlpatterns = [
    url(r'^$', login),
    url(r'^student_home$', student_homepage),
    url(r'^teacher_home$', teacher_homepage),
    url(r'^stuff_home$', stuff_homepage),
    url(r'^manager_home$', manager_homepage),
    url(r'^manager_teacher$', manager_teacher),
    url(r'^manager_student$', manager_student),
    url(r'^logout$', logout),
    url(r'^student_setting$', student_setting),
    url(r'^student_setting/change$', student_setting_change),
    url(r'^teacher_setting$', teacher_setting),
    url(r'^teacher_setting/change$', teacher_setting_change),
    url(r'^stuff_setting$', stuff_setting),
    url(r'^stuff_setting/change$', stuff_setting_change),
    url(r'^register$', register),
    url(r'^section$', section),
    url(r'^teacher_course/$', teacher_course),
    url(r'^student_course/$', student_course),
    url(r'^stuff_course/$', stuff_course),
    url(r'^stuff_look/$', stuff_look),
    url(r'^teacher_delete/$', teacher_delete),
    url(r'^student_delete/$', student_delete),
    url(r'^student_select/$', student_select),

]
