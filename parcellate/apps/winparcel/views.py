from django.views import generic

from rest_framework import (generics)

from .models import Collection, Widget
from .serializers import WidgetSerializer, CollectionSerializer

class CollectionListView(generic.ListView):
    template_name = "collection_list.html"
    def get_queryset(self):
        return Collection.objects.all().order_by('column')


class WidgetListView(generics.ListAPIView):
    serializer_class = WidgetSerializer
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            try:
                collection = Collection.objects.get(uuid=slug)
                return collection.widgets
            except Collection.DoesNotExist:
                pass
        return Collection.objects.none()

class WidgetDetailView(generics.RetrieveAPIView):
    serializer_class = WidgetSerializer
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            return Widget.objects.filter(uuid=slug)
        return Widget.objects.none()

class CollectionDetailView(generics.RetrieveAPIView):
    serializer_class = CollectionSerializer
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            return Collection.objects.filter(uuid=slug)
        return Collection.objects.none()


