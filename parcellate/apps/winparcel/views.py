from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import (View,
                                  CreateView,
                                  UpdateView,
                                  DetailView)

from rest_framework.renderers import JSONRenderer

from .models import BaseObject, Collection, Widget
from .serializers import WidgetSerializer, CollectionSerializer
from .lib import ReadRSS

COLUMNS = 3 #will later be set by a manager, 3 for now though

#
#HttpResponse that returns only JSON
#
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class ParcelView(View):
    template_name = "parcel.html"

    def get(self, request):
        widget_coll = Collection.objects.all()
        obj_cols = dict([(x, []) for x in range(0, COLUMNS)])
        for idx in range(0, COLUMNS):
            obj_cols[idx] = widget_coll.filter(column=idx).order_by('row')
        return render(request,
                      self.template_name,
                      dict(test="TEST", obj_cols=obj_cols)
                     )


@csrf_exempt
class WidgetListView(View):
    def get(self, request):
        widgets = BaseObject.objects.all()
        serializer = WidgetSerializer(widgets, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
class WidgetDetailView(DetailView):
    def get(self, request):
        slug = self.kwargs.get('slug')
        widget = BaseObject.object.get(uuid=slug)
        serializer = WidgetSerializer(widget)
        return JSONResponse(serializer.data)


@csrf_exempt
class CollectionListView(View):
    def get(self, request):
        collections = BaseObject.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
class CollectionDetailView(DetailView):
    def get(self, request):
        slug = self.kwargs.get('slug')
        collection = BaseObject.object.get(uuid=slug)
        serializer = CollectionSerializer(collection)
        return JSONResponse(serializer.data)


class RSSObjectCreateView(CreateView):
    model = RSSObject
    template_name = "add_rss.html"

    def form_valid(self, form):
        response = super(RSSObjectCreateView, self).form_valid(form)
        read_rss = ReadRSS(rss=self.object)
        read_rss.save_entries()
        return response

    def get_success_url(self):
        return reverse("rss-add")


class RSSObjectUpdateView(UpdateView):
    model = RSSObject
    template_name = "add_rss.html"

    def get_success_url(self):
        slug = self.kwargs.get('pk', None)
        if slug:
            return reverse('rss-update', kwargs=dict(pk=slug))
        return reverse("rss-add")

    def get_context_data(self, **kwargs):
        context = super(RSSObjectUpdateView, self).get_context_data(**kwargs)
        context["object_list"] = RSSObject.objects.all()
        return context

