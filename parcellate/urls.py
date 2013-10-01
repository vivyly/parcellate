# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from parcellate.apps.winparcel.views import (ParcelView,
                                             RSSObjectCreateView,
                                             RSSObjectUpdateView,
                                             #RSSObjectListView,
                                             RSSObjectDetailView)
PRIMARY_KEY = """[\w-]+"""

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    #(r'/update$', 'parcellate.apps.winparcel.views.update'),
    url(r'^', include('apps.winparcel.urls')),
    url(r'rss/add$', RSSObjectCreateView.as_view(), name="rss-add"),
    url(r'rss/update/(?P<pk>%s)$' %PRIMARY_KEY,
        RSSObjectUpdateView.as_view(), name="rss-update"),
    url(r'rss/detail$', RSSObjectDetailView.as_view(), name="rss-detail"),
    url(r'$', ParcelView.as_view(), name="parcel-view"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
