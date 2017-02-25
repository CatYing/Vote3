"""Vote3 URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from Vote3 import settings
from django.contrib.staticfiles import views
from cm import views as c_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', c_views.index, name='index'),
    url(r'^login/$', c_views.login, name='login'),
    url(r'^logout/$', c_views.logout, name='logout'),
    url(r'^members/$', c_views.member_list, name='list'),
    url(r'^detail/(?P<member_id>[0-9]+)/$', c_views.member_detail, name='detail'),
    url(r'^voter-rank/$', c_views.voter_rank, name='voter_rank'),
    url(r'^all-rank/$', c_views.all_rank, name='all_rank'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.static.serve, {'document_root': settings.STATIC_ROOT}, name="static"),
        url(r'^media/(?P<path>.*)$', views.static.serve, {'document_root': settings.MEDIA_ROOT}, name="media")
    ]
