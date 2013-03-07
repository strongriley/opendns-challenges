from django.test import TestCase

from shortener.shortenings.models import Shortening
from shortener.phishes.models import PhishUrl


class ShorteningTests(TestCase):
    """
    Test behavior associated with the Shortening Model.
    """
    def test_random_short_id(self):
        """
        Create few hundred URLs, none should be the same.
        More a spot test. The uniqueness on short_id will ensure all's good.
        """
        url = "http://example.com"
        n = 500
        for i in range(n):
            obj = Shortening(url=url)
            obj.full_clean()
            obj.save()
        self.assertEqual(Shortening.objects.filter(url=url).count(), n)

    def test_check_is_safe_true(self):
        PhishUrl.objects.create(phish_id=1, url="http://is-safe-true.com")
        short = Shortening(url="http://opendns.com")
        short.full_clean()
        short.save()
        self.assertTrue(short.check_is_safe())

    def test_check_is_safe_false(self):
        PhishUrl.objects.create(phish_id=1, url="http://facebook.com")
        short = Shortening(url="http://facebook.com")
        short.full_clean()
        short.save()
        self.assertFalse(short.check_is_safe())

    def test_url_visited(self):
        short = Shortening(url="http://rileystrong.com")
        short.full_clean()
        short.save()
        self.assertEqual(short.visits, 0)
        for i in range(10):
            short.url_visited()
        self.assertEqual(short.visits, 10)
