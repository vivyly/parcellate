import urllib2
from urlparse import urlparse

from bs4 import BeautifulSoup

from .models import Collection, Widget

TAG_LIST = {
    'title':'title',
    'link':'url',
    'id':'srcid',
    'guid':'srcid',
    'published':'published',
    'pubDat':'published',
    'updated':'updated',
    'summary':'summary',
    'description':'summary',
    'content':'content',
}

class ReadBase(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get('url', None)
        if self.url:
            self.html = self.get_html()
            self.soup = self.soup(self.html)
            self.collection = self.get_domain_object()

    def get_html(self):
        fstream = urllib2.urlopen(self.url)
        html = fstream.read()
        fstream.close()
        return html

    def set_soup(self, html):
        return BeautifulSoup(html)

    def get_domain_object(self):
        domain_url = 'http://%s' % urlparse(self.url).netloc
        try:
            c = Collection.objects.get(url=domain_url)
        except Collection.DoesNotExist:
            c = self.create_collection(domain_url)
        return c

    def create_collection(self, domain_url):
        c = Collection()
        c.url = domain_url
        c.title = domain_url
        c.status = 'active'
        c.save()
        return c

class ReadRSS(ReadBase):
    def __init__(self, **kwargs):
        self.rss = kwargs.get('rss', None)
        #if isinstance(rss, str): need to create rss obj
        #    self.rss = rss
        if self.rss:
            kwargs['url'] = self.rss.url
        super(ReadRSS, self).__init__(self, **kwargs)

    def save_entries(self):
        taglist = TAG_LIST
        entries_created = 0
        if not self.soup:
            return entries_created
        entries = self.soup.find_all('entry')
        if not entries:
            entries = self.soup.find_all('item')
        print entries
        for entry in entries:
            try:
                rssids = entry.find_all('id')
                if rssids:
                    rssid = rssids[0]
                else:
                    rssguids = entry.find_all('guid')
                    if rssguids:
                        rssid = rssguids[0]
                if rssid:
                    Widget.objects.get(srcid=rssid)
            except Widget.DoesNotExist:
                created = self.create_entry(taglist, entry)
                if created:
                    entries_created += 1
            except IndexError:
                continue
        return entries_created

    def create_entry(self, taglist, entry):
        rss_entry = Widget()
        for tag in taglist.keys():
            try:
                tmp = entry.find_all(tag)[0]
                if tag == 'link' and tmp:
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
            rss_entry.collection = self.rss
            rss_entry.widget_type = 'rss'
            rss_entry.save()
            return True
        return False


class ReadPage(ReadBase):
    def create_widget(self, content):
        try:
            w = Widget.objects.get(url=self.url)
        except Widget.DoesNotExist:
            w = Widget()
            w.url = self.url
            w.title = self.soup.title
            w.content = content
            w.collection = self.collection
            w.widget_type = 'page'
            w.save()

    def save_page(self):
        body = self.soup.body
        content = self.find_content(body)
        self.create_widget(content)

    def find_content(self, node):
        max_text = ""
        if node.children:
            for child in node.children:
                content = self.find_content(child)
                if len(max_text) < len(content):
                    max_text = content
            return max_text
        else:
            return node.text


class ReadSocial(ReadBase):
    def get_domain_object(self):
        try:
            c = Collection.objects.get(url=self.url)
        except Collection.DoesNotExist:
            c = self.create_collection(self.url)
        return c


    def create_content(self):
        pass

    def create_comments(self):
        pass
