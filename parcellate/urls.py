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

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'$', ParcelView.as_view()),
    (r'/update$', 'parcellate.apps.winparcel.views.update'),
    (r'/rss/add$', RSSObjectCreateView.as_view()),
    (r'/rss/update$', RSSObjectUpdateView.as_view()),
    (r'/rss/detail$', RSSObjectDetailView.as_view()),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
