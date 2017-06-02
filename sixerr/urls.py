"""sixerr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from sixerrApp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'gigs/(?P<id>[0-9]+)/$', views.gig_detail, name='gig_detail'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    # url(r'^auth/', include('auth_views.urls', namespace='auth')),
    #login
    url(r'^login/$', auth_views.login, name='login'),
    #logout
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}, name='logout'),
]