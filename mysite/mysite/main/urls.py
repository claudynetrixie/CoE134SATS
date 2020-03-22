"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from django.conf.urls import url

from . import teachers, parents

from rest_framework.urlpatterns import format_suffix_patterns

app_name = "main"

urlpatterns = [
    path("employees/", views.employeeList.as_view()),
    path("", views.homepage, name="homepage"),
    path('tinymce/', include('tinymce.urls')),
    # path("register/", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("login", views.login_request, name="login"),
    path("welcome", views.welcome, name='welcome'),

    path('accounts/signup/parent/', parents.ParentSignUpView.as_view(), name='parent_signup'),
    path('accounts/signup/parent/welcome/', views.welcome_parent, name='parent_welcome'),
    path('students/', views.list_students, name='list_students'),
    path('stud_attendance/', views.stud_attendance, name='stud_attendance'),
    path('child_stats/', views.child_stats, name='child_stats'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),

    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),

    path('accounts/signup/teacher/welcome/', views.welcome, name='teacher_welcome'),
]
