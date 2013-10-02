from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic import (View,
                                  DetailView)

from rest_framework.renderers import JSONRenderer

from .models import Collection, Widget
from .serializers import WidgetSerializer, CollectionSerializer
#from .lib import ReadRSS

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
        widget_collection = Collection.objects.all()
        obj_cols = {}
        for idx in range(0, COLUMNS):
            obj_cols[idx] = widget_collection.filter(column=idx).order_by('row')
        return render(request,
                      self.template_name,
                      dict(test="TEST", obj_cols=obj_cols)
                     )


@csrf_exempt
class WidgetListView(View):
    def get(self, request):
        widgets = Widget.objects.all()
        serializer = WidgetSerializer(widgets, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
class WidgetDetailView(DetailView):
    def get(self, request):
        slug = self.kwargs.get('slug')
        widget = Widget.objects.get(uuid=slug)
        serializer = WidgetSerializer(widget)
        return JSONResponse(serializer.data)


@csrf_exempt
class CollectionListView(View):
    def get(self, request):
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
class CollectionDetailView(DetailView):
    def get(self, request):
        slug = self.kwargs.get('slug')
        collection = Collection.objects.get(uuid=slug)
        serializer = CollectionSerializer(collection)
        return JSONResponse(serializer.data)


