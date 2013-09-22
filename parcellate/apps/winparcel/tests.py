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
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def create_rss(self):
        rss = RSSObject()
        rss.url = 'http://feeds.feedburner.com/seriouseats'
        rss.title = 'Serious Eats'
        rss.save()
        return rss

    def test_add_rss(self):
        self.create_rss()

    def test_add_rss_entry(self):
        testvals = {'title': 'Test Test Test',
                    'url': 'http://www.google.com',
                    'summary': 'This is a test save',
                    'author': 'Viv',
                    'uri': 'http://vivyly.github.io',
                    'content': '<div class="blah">TESTING</div>'
                   }
        rss_obj = self.create_rss()
        rss_entry = RSSEntry()
        for key, val in testvals.iteritems():
            setattr(rss_entry, key, val)
        rss_entry.rssatom = rss_obj
        rss_entry.save()

    def test_add_rss_entry_lib(self):
        pass

