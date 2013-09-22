import urllib2
import urlparse

from django.db import models
from django.template.loader import render_to_string

from json_field import JSONField

class BaseObject(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

###############################################
#
# Site Objects (i.e. any random link)
#
##############################################

class SiteObj(BaseObject):

    def resolve_content(self):
        fstream = urllib2.urlopen(self.url)
        html = fstream.read()
        fstream.close()
        return html

    @property
    def render(self):
        content = self.resolve_content()
        return render_to_string("site_page.html", dict(site=self, content=content))

###############################################
#
# RSS Objects (i.e. pajiba, seriouseats)
#
##############################################

class RSSObject(BaseObject):
    pass

class RSSEntry(BaseObject):
    rssid = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    author_name = models.CharField(blank=True, max_length=255)
    author_uri = models.CharField(blank=True, max_length=255)
    content = models.TextField(blank=True)
    meta = JSONField()
    rssatom = models.ForeignKey(RSSObject)

    @property
    def render(self):
        return render_to_string('entry.html', dict(entry=self, content=self.content))



###############################################
#
# Social Site Objects (i.e. reddit, hacker news)
#
##############################################

class SocialSite(BaseObject):
    pass


class SocialSection(BaseObject):
    srcid = models.CharField(blank=True, max_length=255)
    site = models.ForeignKey(SocialSite)


class SocialLink(BaseObject):
    srcid = models.CharField(blank=True, max_length=255)
    image = models.URLField(blank=True)
    desc = models.TextField(blank=True)
    section = models.ForeignKey(SocialSection)

    def resolve_content(self):
        urldata = urlparse.urlparse(self.url.__str__())
        if 'imgur' in urldata.netloc and self.url.__str__().endswith('.jpg'):
            return """<img src="%s">""" % self.url
        elif self.desc:
            return self.desc
        else:
            return """<iframe class="entry_iframe" src="%s"></iframe>""" % self.url

    @property
    def render(self):
        content = self.resolve_content()
        comment = SocialComments.objects.get(sociallink=self)
        return render_to_string('entry.html',
                                dict(social=self, comment=comment, content=content))


class SocialComments(BaseObject):
    @property
    def render(self):
        fstream = urllib2.urlopen(self.url)
        html = fstream.read()
        fstream.close()
        return html

