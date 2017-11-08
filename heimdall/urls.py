"""help URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from heimdall.views import actions

app_name = 'heimdall'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^heimdall/$', actions.overview, name="overview"),
    url(r'^heimdall/(?:item=(?P<item>[a-z]+))&(?:action=overview)', actions.overview, name="overview"),
    url(r'^heimdall/(?:item=(?P<item>[a-z]+))&(?:action=list)', actions.list, name="list"),
    url(r'^heimdall/(?:item=(?P<item>[a-z]+))&(?:action=save)', actions.save, name="save"),
    url(r'^heimdall/(?:item=(?P<item>[a-z]+))&(?:action=add)', actions.add, name="add"),
    url(r'^heimdall/(?:item=(?P<item>[a-z]+))&(?:action=update)(&(?:id=(?P<id>[0-9]+)))?$', actions.update,
        name="update"),
    url(r'^heimdall/(?:item=(?P<item>[a-z]+))&(?:action=detail)&(?:id=(?P<id>[0-9]+))', actions.detail, name="detail"),
    url(r'^heimdall/(?:item=(?P<item>[a-z]+))&(?:action=remove)&(?:id=(?P<id>[0-9,]+))', actions.remove, name="remove")
    # url(r'^heimdall/(?:item=(?P<item>[a-z]+))&(?:action=(?P<action>[a-z]+))', actions.objectProcessor, name="objectProcessor"),
]
