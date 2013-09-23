"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from .models import (RSSObject,
                     RSSEntry)
from .lib import ReadRSS


class SimpleTest(TestCase):
    test_data = dict(
        url = 'http://feeds.feedburner.com/seriouseats',
        title = 'Serious Eats'
            )

    testvals = {'title': 'Test Test Test',
                    'url': 'http://www.google.com',
                    'summary': 'This is a test save',
                    'author': 'Viv',
                    'uri': 'http://vivyly.github.io',
                    'content': '<div class="blah">TESTING</div>'
                   }
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def create_rss(self):
        rss = RSSObject()
        for key, val in self.test_data.iteritems():
            setattr(rss, key, val)
        rss.save()
        return rss

    def test_add_rss(self):
        rss_obj = self.create_rss()
        for key, val in self.test_data.iteritems():
            self.assertEqual(getattr(rss_obj, key), val)

    def test_add_rss_entry(self):
        rss_obj = self.create_rss()
        rss_entry = RSSEntry()
        for key, val in self.testvals.iteritems():
            setattr(rss_entry, key, val)
        rss_entry.rssatom = rss_obj
        rss_entry.save()
        for key, val in self.test_data.iteritems():
            self.assertEqual(getattr(rss_obj, key), val)

        for key, val in self.testvals.iteritems():
            self.assertEqual(getattr(rss_entry, key), val)

    def test_add_rss_entry_lib(self):
        rss_obj = self.create_rss()
        read_rss = ReadRSS(rss=rss_obj)
        read_rss.save_entries()

