# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from parcellate.apps.winparcel.views import (CollectionListView,
                                             WidgetListView,
                                             WidgetDetailView,
                                             CollectionDetailView,
                                             )

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

SLUG = '''[a-zA-Z0-9_\-]+'''


urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/widget/(?P<slug>%s)/$' %SLUG, WidgetDetailView.as_view(),
                                                name="widget-detail"),
    url(r'^api/widgets/(?P<slug>%s)/$' %SLUG, WidgetListView.as_view(),
                                                name="widget-list"),
    url(r'api/collection/(?P<slug>%s)/$' %SLUG, CollectionDetailView.as_view(),
                                                name="collection-detail"),
    url(r'^', CollectionListView.as_view(), name="collection-list"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
