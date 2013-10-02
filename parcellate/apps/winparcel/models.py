from django.db import models
from django.template.loader import render_to_string

from shortuuidfield import ShortUUIDField
from json_field import JSONField


class BaseObject(models.Model):
    STATUS_CHOICES = [[x, x] for x in ['active',
                                       'hidden',
                                       'deleted',
                                       'saved']]
    uuid = ShortUUIDField(unique=True)
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True, default='')
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES)
    column = models.IntegerField(default=0)
    row = models.IntegerField(default=0)

    class Meta:
        abstract = True


###############################################
#
# Tag Object
#
##############################################
class Tag(models.Model):
    uuid = ShortUUIDField(unique=True)
    name = models.CharField(max_length=255)
    base_object = models.ForeignKey(BaseObject)


###############################################
#
# Collection Object
#
##############################################
class Collection(BaseObject):
    COLLECTION_TYPES = [[x, x] for x in ['rss',
                                         'page',
                                         'social'
                                        ]]
    collection_type = models.CharField(
                        choices=COLLECTION_TYPES)
    json = JSONField(blank=True, default={})

    def __getattr__(self, name):
        try:
            return self.json[name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        self.json[name] = value

    def __delattr__(self, name):
        del self.json[name]

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
    WIDGET_TYPES = [[x, x] for x in ['rss',
                                     'page',
                                     'social',
                                     'comments'
                                    ]]
    widget_type = models.CharField(choices=WIDGET_TYPES)
    collection = models.ForeignKey(Collection)
    srcid = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=255, blank=True, default='')
    content = models.TextField(blank=True, default='')

    @property
    def render(self):
        return render_to_string('entry.html',
                                dict(entry=self))

