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
        self.soup = None
        self.html = None
        self.rss = None
        rss = kwargs.get('rss')
        #if isinstance(rss, str): need to create rss obj
        #    self.rss = rss
        if isinstance(rss, RSSObject):
            self.rss = rss

        if self.rss:
            self.html = self.get_html()
            self.soup = self.set_soup(self.html)

    def get_html(self):
        fstream = urllib2.urlopen(self.rss.url)
        html = fstream.read()
        fstream.close()
        return html

    def set_soup(self, html):
        return BeautifulSoup(html)

    def save_entries(self):
        taglist = TAG_LIST
        entries_created = 0
        if not self.soup:
            return entries_created
        entries = self.soup.find_all('entry')
        for entry in entries:
            try:
                rssid = entry.find_all('id')[0]
                RSSEntry.objects.get(rssid=rssid)
            except RSSEntry.DoesNotExist:
                created = self.create_entry(taglist, entry)
                if created:
                    entries_created += 1
            except IndexError:
                continue
        return entries_created

    def create_entry(self, taglist, entry):
        rss_entry = RSSEntry()
        for tag in taglist.keys():
            try:
                tmp = entry.find_all(tag)[0]
                if tag == 'author' and tmp:
                    try:
                        name = tmp.find_all('name')[0].string
                        setattr(rss_entry, 'author_name', name)
                    except IndexError:
                        pass
                    try:
                        uri = tmp.find_all('uri')[0].string
                        setattr(rss_entry, 'author_uri', uri)
                    except IndexError:
                        pass
                elif tag == 'link' and tmp:
                    try:
                        link_tag = tmp.find_all('link')[0]
                        link_href = link_tag.get('href')
                        setattr(rss_entry, 'url', link_href)
                    except (IndexError, KeyError):
                        pass

                else:
                    setattr(rss_entry, taglist[tag], tmp.string)
            except IndexError:
                continue
        if rss_entry.title:
            rss_entry.rssatom = self.rss
            rss_entry.save()
            return True
        return False
