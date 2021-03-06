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
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    column = models.IntegerField(default=0)
    row = models.IntegerField(default=0)


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
# Collection Object: rss, page, social
#
##############################################
class CollectionType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'CollectionType: %s ' % self.name

class Collection(BaseObject):
    collection_type = models.ForeignKey(CollectionType)
    json = JSONField(blank=True, default={})

    def __unicode__(self):
        return u'Collection: %s ' % self.title

    #default ordering
    @property
    def parcels_old_to_new(self):
        return Parcel.objects.filter(collection=self).order_by('-published')

    #this will only be tied to a switch on the user acct
    @property
    def parcels_new_to_old(self):
        return Parcel.objects.filter(collection=self).order_by('published')

    #return boolean: check for existence without incurring cost of
    # calling every entry
    @property
    def parcels(self):
        entries = Parcel.objects.filter(rssatom=self)
        if entries[:1]:
            return True
        else:
            return False

    def render(self):
        return render_to_string('collection.html',
                                dict(collection=self))

###############################################
#
# Parcel Objects (i.e. any random link)
# rss, page, social, comments
#
##############################################
class ParcelType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'ParcelType: %s ' % self.name

class Parcel(BaseObject):
    parcel_type = models.ForeignKey(ParcelType)
    collection = models.ForeignKey(Collection)
    srcid = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=255, blank=True, default='')
    content = models.TextField(blank=True, null=True, default='')

    def __unicode__(self):
        return u'Parcel: %s ' % self.title

    @property
    def render(self):
        return render_to_string('parcel.html',
                                dict(parcel=self))

