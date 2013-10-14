import urllib2
from urlparse import urlparse

from bs4 import BeautifulSoup


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
    def __init__(self, url, collection_type, widget_type):
        self.url = url
        self.html = None
        self.soup = None
        self.collection = None
        self.collection_title = ''
        cname = collection_type
        self.collection_type = self.create_collection_type(cname)
        wname = widget_type
        self.widget_type = self.create_widget_type(wname)
        if self.url:
            self.html = self.get_html()
            self.soup = self.set_soup(self.html)
            self.collection = self.get_domain_object()

    def get_html(self):
        fstream = urllib2.urlopen(self.url)
        html = fstream.read()
        fstream.close()
        return html

    def set_soup(self, html):
        return BeautifulSoup(html)

    def find_domain_url(self):
        urlpath = urlparse(self.url)
        if urlpath.netloc == 'feeds.feedburner.com':
            self.collection_title = self.soup.find('title')
            domain_url = self.soup.find('link').string
        else:
            domain_url = 'http://%s' % urlpath.netloc
        return domain_url

    def get_domain_object(self):
        from .models import Collection
        domain_url = self.find_domain_url()
        try:
            c = Collection.objects.get(url=domain_url)
        except Collection.DoesNotExist:
            c = self.create_collection(domain_url)
        return c

    def create_collection_type(self, name):
        from .models import CollectionType
        ctype = CollectionType()
        ctype.name = name
        ctype.save()
        return ctype

    def create_widget_type(self, name):
        from .models import WidgetType
        wtype = WidgetType()
        wtype.name = name
        wtype.save()
        return wtype

    def create_collection(self, domain_url):
        from .models import Collection
        ctype = self.create_collection_type(self.collection_type)
        c = Collection()
        c.url = domain_url
        c.title = self.collection_title or domain_url
        c.status = 'active'
        c.collection_type = ctype
        c.save()
        return c

class ReadRSS(ReadBase):
    def __init__(self, url):
        from .models import Collection, WidgetType
        if isinstance(url, str):
            super(ReadRSS, self).__init__(url, 'rss', 'rss')
        elif isinstance(url, Collection):
            collection = url
            self.url = collection.url
            self.html = self.get_html()
            self.soup = self.set_soup(self.html)
            self.collection = collection
            self.collection_type = collection.collection_type
            self.widget_type = WidgetType.objects.get(name='rss')


    def save_entries(self):
        from .models import Widget
        taglist = TAG_LIST
        entries_created = 0
        if not self.soup:
            return entries_created
        entries = self.soup.find_all('entry')
        if not entries:
            entries = self.soup.find_all('item')
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
        from .models import Widget
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
            if not rss_entry.url:
                rss_entry.url = rss_entry.srcid
            rss_entry.status = 'active'
            rss_entry.collection = self.collection
            rss_entry.widget_type = self.widget_type
            rss_entry.save()
            return True
        return False


class ReadPage(ReadBase):
    def __init__(self, **kwargs):
        kwargs['collection_type'] = 'page'
        kwargs['widget_type'] = 'page'
        super(ReadPage, self).__init__(**kwargs)

    def create_widget(self, content):
        from .models import Widget
        try:
            w = Widget.objects.get(url=self.url)
        except Widget.DoesNotExist:
            w = Widget()
            w.url = self.url
            w.title = self.soup.title
            w.content = content
            w.collection = self.collection
            w.widget_type = self.widget_type
            w.save()

    def save_page(self):
        body = self.soup.body
        content = self.find_content(body)
        self.create_widget(content)

    def find_content(self, node):
        max_text = ""
        children_list = getattr(node, 'children', [])
        if children_list:
            for child in children_list:
                content = self.find_content(child)
                if len(max_text) < len(content):
                    max_text = content
            return max_text
        else:
            try:
                text = node.text
            except AttributeError:
                print node.__str__()
            return text


class ReadSocial(ReadBase):
    def get_domain_object(self):
        from .models import Collection
        try:
            c = Collection.objects.get(url=self.url)
        except Collection.DoesNotExist:
            c = self.create_collection(self.url)
        return c


    def create_content(self):
        pass

    def create_comments(self):
        pass
