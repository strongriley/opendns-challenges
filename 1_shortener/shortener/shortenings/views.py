from django.views.generic import CreateView

from shortener.shortenings.models import Shortening


class ShorteningCreate(CreateView):
    model = Shortening
    template_name = 'index.html'
