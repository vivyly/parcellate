import urlparse
import urllib2

from bs4 import BeautifulSoup

class RSSEntry(object):
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.link = kwargs.get('link')
        self.id = kwargs.get('id')
        self.published = kwargs.get('published')
        self.updated = kwargs.get('updated')
        self.summary = kwargs.get('summary')
        self.author_name = kwargs.get('author_name')
        self.author_uri = kwargs.get('author_uri')
        self.content = kwargs.get('content')
        self.meta = kwargs.get('meta')


class RSSObject(object):
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.link = kwargs.get('link')
        self.id = kwargs.get('id')
        self.updated = kwargs.get('updated')
        self.atom = kwargs.get('atom')
        self.entries = kwargs.get('entries')

class ParcelBase(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.render_html = True

class ParcelNoHeader(ParcelBase):
    name = ''

    def __init__(self, **kwargs):
        super(ParcelBase, self).__init__(kwargs)
        self.render_html = False
        self.html = self.read_url()
        self.soup = self.set_soup(self.html)
        self.rss_url = self.find_rss()
        self.rss = self.handle_rss()


    def read_url(self):
        fstream = urllib2.urlopen(self.url)
        return fstream.read()

    def set_soup(self, html):
        return BeautifulSoup(html)

    def find_rss(self, page_name=None):
        if self.rss_url:
            return self.rss_url
        else:
            if page_name:
                return 'http://feeds.feedburner.com/%s' %page_name
            elif self.name
                return 'http://feeds.feedburner.com/%s' %self.name
        return ''

    def handle_rss(self):
        if not self.rss_url:
            return None
        rss_data = self.read_url(self.rss_url)



class ParcelPajiba(ParcelNoHeader):
    name = 'pajiba'
    domain = 'www.pajiba.com'

    def __init__(self, **kwargs):
        self.rss_url = 'http://feeds.feedburner.com/Pajiba'
        super(ParcelNoHeader, self).__init__(kwargs)

    @property
    def render(self):
        content_class = self.soup.find_all('div', class_='content')
        if content_class:
            return content_class[0]
        return ''


class ParcelSeriousEats(ParcelNoHeader):
    name = 'seriouseats'
    domain = 'www.seriouseats.com'

    def __init__(self, **kwargs):
        self.rss_url = 'www.seriouseats.com/feeds'
        super(ParcelNoHeader, self).__init__(kwargs)

    @property
    def render(self):
        content_class = self.soup.find_all('section', class_='content-unit')
        if content_class:
            return content_class[0]
        return ''

class ParcelFactory(object):
