import praw
import urllib2
from urlparse import urlparse

from bs4 import BeautifulSoup
from goose import Goose

from passcodes import (REDDIT_USERNAME,
                       REDDIT_PASSWORD)

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
    def __init__(self, url):
        self.url = url
        self.html = self.get_html()
        self.soup = self.set_soup(self.html)

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
            title = self.soup.find('title')
            domain_url = self.soup.find('link').string
        else:
            title = ''
            domain_url = 'http://%s' % urlpath.netloc
        return domain_url, title



#TODO: This is silly, look into building RSS XML to JSON parser
class ReadRSS(ReadBase):
    taglist = TAG_LIST

    def __init__(self, url):
        super(ReadRSS, self).__init__(url)
        self.entry_list = {}
        self.rss_entries = []

    def find_entries(self):
        if self.soup:
            self.rss_entries = self.soup.find_all('entry')
            if not self.rss_entries:
                self.rss_entries = self.soup.find_all('item')

    def parse_entries(self):
        self.find_entries()
        for entry in self.rss_entries:
            rssids = entry.find_all('id')
            if rssids:
                rssid = rssids[0]
            else:
                rssguids = entry.find_all('guid')
                if rssguids:
                    rssid = rssguids[0]
            if rssid:
                key = str(rssid.string)
                self.entry_list[key] = self.parse_entry(entry)
        return self.entry_list

    def parse_entry(self, entry):
        entry_data = {}
        for tag, value in self.taglist.iteritems():
            try:
                entry_tags = entry.find_all(tag)[0]
            except (IndexError, KeyError):
                continue
            if tag == 'link' and entry_tags:
                try:
                    link_tag = entry_tags.find_all('link')[0]
                    entry_data['url'] = link_tag.get('href')
                except (IndexError, KeyError):
                    pass
            else:
                entry_data[value] = entry_tags.string
        return entry_data


class ReadPage(ReadBase):
    def __init__(self, **kwargs):
        super(ReadPage, self).__init__(**kwargs)
        self.article = self.get_article_reader()

    def get_article_reader(self):
        g = Goose()
        return g.extract(url=self.url)

    def find_content(self):
        content = '%s\n' % self.article.cleaned_text
        for movie in self.article.movies:
            content += "%s\n" % movie.embed_code
        return dict(url = self.url,
                    title = self.article.title,
                    summary = self.article.meta_description,
                    content = content)



class ReadReddit(object):
    def __init__(self):
        self.redditor = praw.Reddit(user_agent='my_reddit_parcel')
        self.redditor.login(username=REDDIT_USERNAME, password=REDDIT_PASSWORD)

    def get_front_page(self):
        fplist = []
        for submission in self.redditor.get_front_page():
            key = "%s|%s" % (submission.subreddit_id, submission.id)
            selftext = submission.selftext_html
            if selftext:
                content = selftext
            else:
                content = submission.url
            fplist[key] = dict(title=submission.title,
                               content=content)

