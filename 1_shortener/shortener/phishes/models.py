from django.db import models


class PhishUrl(models.Model):
    """
    Verified malicious URL from phishtank.com
    http://www.phishtank.com/developer_info.php
    """
    phish_id = models.IntegerField(unique=True)
    url = models.URLField(max_length=2048, unique=True)
    inserted = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'inserted'

    def __unicode__(self):
        return self.url
