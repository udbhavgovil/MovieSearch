from django.conf.urls import patterns, include, url
from django.contrib import admin
from core import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MovieSearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register',views.register),
    url(r'^index', views.login),
    url(r'^logout',views.logout),
    url(r'^movie.html/(?P<MovieId>[0-9]+)$',views.add_movie),
    url(r'^movie.html/r(?P<MovieId>[0-9]+)$',views.remove_movie),
    url(r'^movie', views.search_movie),
    url(r'^$', views.startup),
) 
