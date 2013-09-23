import urllib2

from bs4 import BeautifulSoup

from .models import RSSObject, RSSEntry

class ParcelWindow(object):
    def __init__(self, **kwargs):
        self.parcel_obj = kwargs.get('parcel_obj')

    @property
    def render(self):
        return self.parcel_obj.render()

TAG_LIST = {
    'title':'title',
    'link':'url',
    'id':'rssid',
    'published':'published',
    'updated':'updated',
    'summary':'summary',
    'author':'',
    'content':'content',
}

class ReadRSS(object):
    def __init__(self, **kwargs):
        rss = kwargs.get('rss')
        if isinstance(rss, str):
            self.rss = rss
        elif isinstance(rss, RSSObject):
            self.rss = rss.url

        if self.rss:
            self.html = self.get_html()
            self.soup = self.set_soup(self.html)

    def get_html(self):
        fstream = urllib2.urlopen(self.rss)
        html = fstream.read()
        fstream.close()
        return html

    def set_soup(self, html):
        return BeautifulSoup(html)

    def save_entries(self):
        taglist = TAG_LIST
        entries = self.soup.findall('entry')
        for entry in entries:
            try:
                rssid = entry.findall('id')[0]
                RSSEntry.objects.get(rssid=rssid)
            except RSSEntry.DoesNotExist:
                self.create_entry(taglist, entry)
            except IndexError:
                continue

    def create_entry(self, taglist, entry):
        rss_entry = RSSEntry()
        for tag in taglist.keys():
            try:
                tmp = entry.findall(tag)[0]
                if tag == 'author':
                    try:
                        name = tmp.findall('name')[0]
                        setattr(rss_entry, 'author_name', name)
                    except IndexError:
                        pass
                    try:
                        uri = tmp.findall('uri')[0]
                        setattr(rss_entry, 'author_uri', uri)
                    except IndexError:
                        pass
                else:
                    setattr(rss_entry, taglist[tag], tmp)
            except IndexError:
                continue
        if rss_entry.title:
            rss_entry.save()
        return None
