from django.views import generic

from rest_framework import (generics)

from .models import Collection, Widget
from .serializers import WidgetSerializer, CollectionSerializer
from .lib import ReadRSS

class CollectionListView(generic.ListView):
    template_name = "collection_list.html"
    def get_queryset(self):
        return Collection.objects.all().order_by('column')


class CollectionCreateView(generics.CreateAPIView):
    def post_save(self, obj, created=False):
        if created:
            reader = ReadRSS(obj)
            reader.save_entries()


class WidgetListView(generics.ListAPIView):
    model = Widget
    serializer_class = WidgetSerializer
    def get_queryset(self):
        uuid = self.kwargs.get('uuid')
        if uuid:
            try:
                collection = Collection.objects.get(uuid=uuid)
                return collection.widgets_old_to_new
            except Collection.DoesNotExist:
                pass
        return Collection.objects.none()

class WidgetDetailView(generics.RetrieveAPIView):
    model = Widget
    serializer_class = WidgetSerializer
    lookup_field = 'uuid'
    def get_queryset(self):
        uuid = self.kwargs.get('uuid')
        if uuid:
            return Widget.objects.filter(uuid=uuid)
        return Widget.objects.none()


class WidgetDestroyView(generics.DestroyAPIView):
    pass


class CollectionDetailView(generics.RetrieveAPIView):
    model = Collection
    serializer_class = CollectionSerializer
    lookup_field = 'uuid'
    def get_queryset(self):
        uuid = self.kwargs.get('uuid')
        if uuid:
            return Collection.objects.filter(uuid=uuid)
        return Collection.objects.none()


