from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import RedirectView

from shortener.shortenings.forms import ShorteningForm
from shortener.shortenings.models import Shortening


class ShorteningCreateView(CreateView):
    form_class = ShorteningForm
    template_name = 'index.html'


class ShorteningDetailView(DetailView):
    model = Shortening
    template_name = 'detail.html'
    slug_field = 'short_id'
    slug_url_kwarg = 'short_id'


class ProtectedRedirectView(RedirectView, ShorteningDetailView):
    permanent = False
    query_string = False
    template_name = 'phish.html'

    def get(self, request, *args, **kwargs):
        """
        If link is not blocked, use standard redirect.
        If blocked, use DetailView.
        """
        self.object = self.get_object()
        if self.object.check_is_safe():
            self.object.url_visited()
            return super(ProtectedRedirectView, self).get(request,
                                                          *args, **kwargs)

        # Code taken from django.views.generic.detail.BaseCreateView
        # since couldn't do that complicated of multiple inheritence.
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_redirect_url(self, short_id):
        return self.object.url
