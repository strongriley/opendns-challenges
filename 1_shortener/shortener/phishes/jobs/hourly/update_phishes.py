import os
import urllib2
import json
from datetime import datetime

from django.conf import settings
from django_extensions.management.jobs import HourlyJob

from shortener.phishes.models import PhishUrl


class Job(HourlyJob):
    """
    Updates Phish records. For speed, we use our own DB records taken from
    phishtank.com and we won't hit their API limit.
    """
    help = "Update the PhishUrls and PhishDomains"

    def execute(self):
        # Determine where to start in the phishtank parsed file.
        count = PhishUrl.objects.count()
        latest_entry = None
        latest = None
        if count:
            latest_entry = PhishUrl.objects.latest()
            latest = latest_entry.inserted

        # Get the data from the server.
        # This will take a while - it's a big file.
        # TODO: optimize to save to filesystem, avoid memory hogging.
        # TODO: error logging?

        # Debugging shortcut: look for the file locally.
        # Only in debug mode and on first run. Just too tedious to download
        # 50 MB every time.
        path = os.path.join(settings.SRC_PATH, 'verified_online.json')
        if settings.DEBUG and not latest and os.path.isfile(path):
            print "Using debugging file"
            with open(path) as f:  # Cleanup and close
                raw_json = f.read()
        else:
            print "Downloading file (This may take a while)."
            raw_json = urllib2.urlopen(settings.PHISHTANK_JSON_URL).read()

        # Prepare data for insertion.
        # insertion time based on verification_time since only verified
        # entries appear.
        parsed = json.loads(raw_json)
        if latest:
            # TODO with more understanding of file, could skip lots of entries
            # if the file is ordered
            for entry in parsed:
                # TODO refactor with dateutil, but trying to stick with pure
                # python - fewer extensions.
                entry['inserted'] = datetime.strptime(
                    entry['verification_time'][:-6],
                    '%Y-%m-%dT%H:%M:%S')
                entry['inserted'] = entry['inserted'].replace(
                    tzinfo=latest.tzinfo)
            parsed = [url for url in parsed if url['inserted'] > latest]

        # Bulk insert to save the database.
        id = latest_entry.pk + 1 if latest_entry else 1
        urls = []
        for entry in parsed:
            urls.append(PhishUrl(pk=id,
                                 phish_id=entry['phish_id'],
                                 url=entry['url']))
            id = id + 1
        # Limit batch size to 500 because of sqlite constraints.
        # http://stackoverflow.com/a/9527898/561956
        PhishUrl.objects.bulk_create(urls, batch_size=500)
