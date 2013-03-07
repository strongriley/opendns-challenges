from django.db import models


class Shortening(models.Model):
    """
    A shortened URL for twitter or app.net.
    Phish detection is done when the URL is visited - not submitted.
    This allows blocking after submission.
    """
    short_id = models.CharField(max_length=8, unique=True)
    url = models.CharField(max_length=2048)
    visits = models.IntegerField(default=0, editable=False)
    is_blocked = models.BooleanField()
