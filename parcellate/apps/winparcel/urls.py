from django.conf.urls import patterns, url
from .views import WidgetListView, WidgetDetailView


urlpatterns = patterns('winparcel.views',
    url(r'^widget/$', WidgetListView.as_view(), name="widget-list"),
    url(r'^widget/(?P<slug>[\w_]+)/$', WidgetDetailView.as_view(),
                                                name="widget-detail"),
)
