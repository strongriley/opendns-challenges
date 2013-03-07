import random

from django.db import models
from django.conf import settings


def generate_short_id():
    """
    Returns an 8-character random string that is not yet in the database.
    """
    while True:
        short_id = ''.join([random.choice(settings.ALLOWED_CHARACTERS)
            for i in range(8)])
        if Shortening.objects.filter(short_id=short_id).count() == 0:
            return short_id


class Shortening(models.Model):
    """
    A shortened URL for twitter or app.net.
    Phish detection is done when the URL is visited - not submitted.
    This allows blocking after submission.
    """
    short_id = models.CharField(max_length=8, unique=True,
                                default=generate_short_id)
    url = models.URLField(max_length=2048)
    visits = models.IntegerField(default=0, editable=False)
    is_blocked = models.BooleanField()

    def __unicode__(self):
        return '%s: %s' % ((self.short_id, self.url))

    def get_absolute_url(self):
        return '/%s/detail/' % self.short_id
