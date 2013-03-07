from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from shortener.shortenings.views import ShorteningCreate

urlpatterns = patterns('',
    url(r'^$',ShorteningCreate.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
