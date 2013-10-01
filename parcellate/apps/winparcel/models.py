import urllib2
import urlparse

from django.db import models
from django.template.loader import render_to_string

from shortuuidfield import ShortUUIDField
from json_field import JSONField
from bs4 import BeautifulSoup


class BaseObject(models.Model):
    uuid = ShortUUIDField(unique=True)
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True, default='')
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField()
    column = models.IntegerField(default=1)
    row = models.IntegerField(default=0)

    class Meta:
        abstract = True


###############################################
#
# Collection Object
#
##############################################
class Collection(BaseObject):
    json = JSONField(blank=True, default={})
    #default ordering
    @property
    def entries_old_to_new(self):
        entries = Widget.objects.filter(rssatom=self).order_by('-published')
        return entries

    #this will only be tied to a switch on the user acct
    @property
    def entries_new_to_old(self):
        entries = Widget.objects.filter(rssatom=self).order_by('published')
        return entries

    #return boolean: check for existence without incurring cost of
    # calling every entry
    @property
    def entries(self):
        entries = Widget.objects.filter(rssatom=self)
        if entries[:1]:
            return True
        else:
            return False

    #@property
    #def render(self):
    #    return render_to_string('rss_object.html',
    #                            dict(rss_object=self))

###############################################
#
# Widget Objects (i.e. any random link)
#
##############################################
class Widget(BaseObject):
    srcid = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=255, blank=True, default='')
    content = models.TextField(blank=True, default='')

    @property
    def render(self):
        return render_to_string('entry.html',
                                dict(entry=self))

###############################################
#
# Site Objects (i.e. any random link)
#
##############################################

#class SiteDomain(BaseObject):
#    content_tag = models.CharField(blank=True, max_length=255)
#    content_attr = models.CharField(blank=True, max_length=255)
#    content_val = models.CharField(blank=True, max_length=255)
#
#class SiteObj(BaseObject):
#    parsed_block = models.TextField(blank=True)
#    domain = models.ForeignKey(SiteDomain)
#
#    def resolve_content(self):
#        html = ''
#        try:
#            fstream = urllib2.urlopen(self.url)
#            html = fstream.read()
#            fstream.close()
#        except urllib2.URLError:
#            pass
#        return html
#
#    def parse_content(self, content):
#        soup = BeautifulSoup(content)
#        params = {self.domain.content_attr: self.domain.content_val}
#        contentblock = soup.find(self.domain.content_tag, **params)
#        return contentblock
#
#    @property
#    def render(self):
#        content = self.resolve_content()
#        if self.domain and self.domain.content_tag:
#            content = self.parse_content(content)
#        return render_to_string("site_page.html", dict(site=self, content=content))


###############################################
#
# Social Site Objects (i.e. reddit, hacker news)
#
##############################################

#class SocialSite(BaseObject):
#    pass
#
#
#class SocialSection(BaseObject):
#    srcid = models.CharField(blank=True, max_length=255)
#    site = models.ForeignKey(SocialSite)
#
#
#class SocialLink(BaseObject):
#    srcid = models.CharField(blank=True, max_length=255)
#    image = models.URLField(blank=True)
#    desc = models.TextField(blank=True)
#    section = models.ForeignKey(SocialSection)
#
#    def resolve_content(self):
#        urldata = urlparse.urlparse(self.url.__str__())
#        if 'imgur' in urldata.netloc and self.url.__str__().endswith('.jpg'):
#            return """<img src="%s">""" % self.url
#        elif self.desc:
#            return self.desc
#        else:
#            return """<iframe class="entry_iframe" src="%s"></iframe>""" % self.url
#
#    @property
#    def render(self):
#        content = self.resolve_content()
#        comment = SocialComments.objects.get(sociallink=self)
#        return render_to_string('entry.html',
#                                dict(social=self, comment=comment, content=content))
#
#
#class SocialComments(BaseObject):
#    comment_tag = models.CharField(blank=True, max_length=255)
#    comment_attr = models.CharField(blank=True, max_length=255)
#    comment_val = models.CharField(blank=True, max_length=255)
#
#    @property
#    def render(self):
#        fstream = urllib2.urlopen(self.url)
#        html = fstream.read()
#        fstream.close()
#        return html

