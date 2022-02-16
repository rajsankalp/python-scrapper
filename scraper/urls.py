"""crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from scraper import views 

urlpatterns = [
    path('', views.index),
    path('profile/', views.profile),
    path('script-link-2/', views.link2),
    path('script-profile-2/', views.profile2),
    path('script-profile-3/', views.index3),
    path('tierheim_gesucht_link_crawler/', views.tierheim_gesucht_link_crawler),
    path('tierheim_gesucht_detail_crawler/', views.tierheim_gesucht_detail_crawler),
    
]
