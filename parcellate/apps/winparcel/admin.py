#/usr/bin/env python
from django.contrib import admin
from parcellate.apps.winparcel.models import (Collection,
                                              CollectionType,
                                              Widget,
                                              WidgetType,
                                              Tag)

class CollectionAdmin(admin.ModelAdmin):
    fields = ['url', 'title', 'status', 'column', 'row', 'collection_type', 'json']


class CollectionTypeAdmin(admin.ModelAdmin):
    fields = ['name']

class WidgetAdmin(admin.ModelAdmin):
    fields = ['url', 'title', 'status', 'column', 'row', 'widget_type',
                    'collection', 'srcid', 'summary', 'content']

class WidgetTypeAdmin(admin.ModelAdmin):
    fields = ['name']


class TagAdmin(admin.ModelAdmin):
    fields = ['name', 'base_object']

admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionType, CollectionTypeAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(WidgetType, WidgetTypeAdmin)
admin.site.register(Tag, TagAdmin)
