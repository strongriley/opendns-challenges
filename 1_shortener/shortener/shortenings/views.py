from django.views.generic import CreateView

from shortener.shortenings.models import Shortening


class ShorteningCreate(CreateView):
    model = Shortening
    template_name = 'index.html'


class ProtectedRedirectView(RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, short_id):
        shortening = get_object_or_404(Shortening, short_id=short_id)
        raise TypeError("not ready!")
