from django.db import models


class Shortening(models.Model):
    url = models.CharField(max_length=2048)
    visits = models.IntegerField(default=0, editable=False)
    is_blocked = models.BooleanField(editable=False)
