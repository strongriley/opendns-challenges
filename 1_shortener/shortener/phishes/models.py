from django.db import models


class PhishUrl(models.Model):
    """
    Verified malicious URL from phishtank.com
    http://www.phishtank.com/developer_info.php
    """
    phish_id = models.IntegerField()
    url = models.CharField(max_length=2048, unique=True)
    inserted = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'inserted'

    def __unicode__(self):
        return self.url


class PhishDomain(models.Model):
    """
    For simplified blacklisting, a domain that has at least 1
    verified phishing URL under it.

    Any shortenings matching a domain will not be allowed.
    """
    domain_name = models.CharField(max_length=2048, unique=True)
    inserted = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'inserted'

    def __unicode__(self):
        return self.domain_name
