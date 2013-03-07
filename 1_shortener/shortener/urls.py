from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from shortener.shortenings.views import ShorteningCreateView
from shortener.shortenings.views import ProtectedRedirectView
from shortener.shortenings.views import ShorteningDetailView


urlpatterns = patterns('',
    url(r'^$',ShorteningCreateView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<short_id>[a-zA-Z0-9]+)/$', ProtectedRedirectView.as_view()),
    url(r'^(?P<short_id>[a-zA-Z0-9]+)/detail$',
        ShorteningDetailView.as_view()),
)
