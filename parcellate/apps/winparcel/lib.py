import urlparse
import urllib2

from bs4 import BeautifulSoup

class ParcelWindow(object):
    def __init__(self, **kwargs):
        self.parcel_obj = kwargs.get('parcel_obj')

    @property
    def render(self):
        return self.parcel_obj.render()


class ReadRSS(object):
    def __init__(self, **kwargs):
        self.rss = kwargs.get('rss')
        self.html = self.get_html()
        self.soup = self.set_soup(self.html)

    def get_html(self):
        fstream = urllib2.urlopen(self.rss.url)
        html = fstream.read()
        fstream.close()
        return html

    def set_soup(self, html):
        return BeautifulSoup(html)



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

