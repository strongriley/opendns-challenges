import os
import urllib2
import json
from datetime import datetime

from django.conf import settings
from django_extensions.management.jobs import HourlyJob

from shortener.phishes.models import PhishUrl
from shortener.phishes.models import PhishDomain


class Job(HourlyJob):
    """
    Updates Phish records. For speed, we use our own DB records taken from
    phishtank.com and we won't hit their API limit.
    """
    help = "Update the PhishUrls and PhishDomains"

    def execute(self):
        # Determine where to start in the phishtank parsed file.
        count = PhishDomain.objects.count()
        if count:
            latest = PhishDomain.objects.latest().inserted
        else:
            latest = False

        # Get the data from the server.
        # This will take a while - it's a big file.
        # TODO: optimize to save to filesystem, avoid memory hogging.
        # TODO: error logging?

        # Debugging shortcut: look for the file locally.
        # Only in debug mode and on first run. Just too tedious to download
        # 50 MB every time.
        path = os.path.join(settings.SRC_PATH, 'verified_online.json')
        if settings.DEBUG and not latest and os.path.isfile(path):
            with open(path) as f:  # Cleanup and close
                raw_json = f.read()
        else:
            raw_json = urllib2.urlopen(settings.PHISHTANK_JSON_URL).open()

        # Prepare data for insertion
        # insertion time based on verification_time.
        parsed = json.loads(raw_json)
        if latest:
            # TODO with more understanding of file, could skip lots of entries
            # after the 1st pass, potentially O(log(n)) instead of O(n) efficiency
            # if the file is timestamp-ordered.
            for entry in parsed:
                parsed['inserted'] = datetime.strptime(entry['verification_time'])
            parsed = [url for url in parsed if url.inserted > latest]

        # Bulk insert to save the database
        urls = []
        for entry in parsed:
            urls.append(PhishUrl(url=entry['url']))
        PhishUrl.objects.bulk_create(urls)
