from django import forms

from shortener.shortenings.models import Shortening


class ShorteningForm(forms.ModelForm):
    class Meta:
        model = Shortening
        fields = ('url',)
