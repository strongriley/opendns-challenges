from django.contrib import admin

from shortener.phishes.models import PhishUrl
from shortener.phishes.models import PhishDomain

admin.site.register(PhishUrl)
admin.site.register(PhishDomain)
