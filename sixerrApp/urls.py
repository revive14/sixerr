from django.conf.urls import url
from sixerrApp import views

urlpatterns= [
#GIG DETAILS PAGE
    url(r'gigs/(?P<id>[0-9]+)/$', views.gig_detail, name='gig_detail'),
#CREATE A GIG PAGE
    url(r'^create_gig/$', views.create_gig, name='create_gig'),
#MY GIGS PAGE
    url(r'^my_gigs/$', views.my_gigs, name='my_gigs'),
#EDIT GIG
    url(r'edit_gig/(?P<id>[0-9]+)/$', views.edit_gig, name='edit_gig'),
]
