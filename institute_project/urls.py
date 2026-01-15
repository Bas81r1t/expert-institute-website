"""
URL configuration for institute_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # CHANGE: name='student_login' ko badal kar name='login' kar diya
    path('student-login/', views.student_login, name='login'), 
    
    path('my-profile/', views.student_profile, name='student_profile'),
    path('student-logout/', views.student_logout, name='student_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('donate/', views.donate, name='donate'),
    path('courses/', views.courses, name='courses'),
    path('admission/', views.admission, name='admission'),
]