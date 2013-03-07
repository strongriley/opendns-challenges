from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404

from shortener.shortenings.forms import ShorteningForm
from shortener.shortenings.models import Shortening


class ShorteningCreateView(CreateView):
    form_class = ShorteningForm
    template_name = 'index.html'


class ProtectedRedirectView(RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, short_id):
        shortening = get_object_or_404(Shortening, short_id=short_id)
        raise TypeError("not ready!")


class ShorteningDetailView(DetailView):
    model = Shortening
    template_name = 'detail.html'
    slug_field = 'short_id'
    slug_url_kwarg = 'short_id'
